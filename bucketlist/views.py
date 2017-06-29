from flask import render_template, request, redirect, url_for, session, flash, Markup

from bucketlist import app, classes
from .forms import SignUpForm, LoginForm, BucketlistForm, ActivityForm, BucketlistFormUpdate, ActivityFormUpdate
import hashlib
from .classes import all_users, all_bucketlists, all_bucketlists_activities

global current_user
current_user = []


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/auth/', methods=['GET', 'POST'])
def new_user_login():

    form = LoginForm(request.form)

    if form.validate_on_submit():

        hash_object = hashlib.sha1(request.form.get('password').encode())
        entered_password = hash_object.hexdigest()

        #User exists
        if request.form.get('email') in all_users:

            if all_users[request.form.get('email')][2] == entered_password:

                set_current_user(all_users[request.form.get('email')])

                return redirect(url_for('user_bucket_lists'))
            else:
                error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Invalid Credentials! </strong>Either your email or password is wrong!\
                        Please enter correct credentials!\
                        </div>")

                flash(error)
                return render_template("login.html", form=LoginForm())

        else:
            error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Invalid Credentials!</strong> Either your email or password is wrong!\
                        Please enter correct credentials!\
                        </div>")
            flash(error)
            return render_template("login.html", form=LoginForm())


    else:
        return render_template("login.html", form=LoginForm())

## Set user details on login
def set_current_user(user_details):

    global current_user
    current_user = user_details

## Get user details
def check_current_user():
    logged_in = False

    global current_user

    details_count = len(current_user)

    if details_count == 0:
        logged_in = False
    else:
        logged_in = True

    return logged_in


@app.route("/sign-up")
def signup():
    form = SignUpForm()
    return render_template("sign_up.html", form=form)


@app.route("/sign-up/new-user", methods=['GET', 'POST'])
def create_user():

    form = SignUpForm(request.form)

    if form.validate_on_submit():

        if request.form.get('email') in all_users:

            error = Markup("<div class='alert alert-danger' role='alert'>\
                            <strong>User Exisits!</strong> The Email entered already exists!\
                            </div>")
            flash(error)
            return redirect(url_for("signup"))

        else:
            user = classes.User()
            user.create_user(request.form.get('fullname'),
                             request.form.get('email'), request.form.get('password'))

            success = Markup("<div class='alert alert-success' role='alert'>\
                            <strong>Done! </strong>You have successfully registered! Kindly Login\
                            </div>")

            flash(success)

            form_login = LoginForm()
            return render_template("login.html", form=form_login)

    return render_template("sign_up.html", form=form)


# Log out and set the current user to empty list
@app.route("/logout")
def logout():
    global current_user
    current_user = []

    return redirect(url_for('index'))


############################# Bucketlist functions

@app.route("/my-bucketlists/")
def user_bucket_lists():

    if check_current_user() is True:

        #Check if user has bucketlist already
        if current_user[1] in all_bucketlists:
            return render_template('view_bucket_lists.html', user=current_user,
                                   bucketlists=all_bucketlists[current_user[1]])

        else:
            return render_template('view_bucket_lists.html', user=current_user)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))


@app.route("/add-bucketlist")
def add_bucketlist():
    if check_current_user() is True:
        form = BucketlistForm()
        return render_template("add_bucket_list.html", form=form)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))



@app.route("/create-bucketlist", methods=['GET', 'POST'])
def create_bucketlist():
    form = BucketlistForm()

    global current_user

    if request.method == "POST" and form.validate_on_submit():

        bucketlist = classes.Bucketlist()
        bucketlist.create_bucketlist(current_user[1], request.form.get("bucketlistname"),
                                     request.form.get("simple_description"))

        success = Markup("<div class='alert alert-success' role='alert'>\
                        <strong>Done! </strong>Your "+request.form.get("bucketlistname")+"\
                         Bucketlist is created.</div>")
        flash(success)

        return render_template('view_bucket_lists.html',
                               bucketlists=all_bucketlists[current_user[1]],
                               user=current_user)

    return render_template('view_bucket_lists.html', form=form)


@app.route("/change-bucketlist/<id>")
def change_bucketlist(id):
    if check_current_user() is True:  

        global current_user
        bucketlist_detail = all_bucketlists[current_user[1]][int(id)]
        bucketlist_id = int(id)

        form = BucketlistFormUpdate()

        for key, value in bucketlist_detail.items():
            form.bucketlistname.data = key
            form.simple_description.data = value

        return render_template("change_bucket_list.html", form=form, bucketlist_id=bucketlist_id)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))

@app.route("/update-buckelist/<id>", methods=['GET', 'POST'])
def update_bucketlist(id):
    if check_current_user() is True:

        form = BucketlistFormUpdate(request.form)

        if form.validate_on_submit():
            global current_user

            bucketlist = classes.Bucketlist()
            bucketlist.update_bucketlist(current_user[1], int(id),
                                         request.form.get("bucketlistname"),
                                         request.form.get("simple_description"))

            return redirect(url_for("user_bucket_lists"))

        else:
            return render_template("change_bucket_list.html", form=form)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))


@app.route("/delete-bucketlist/<id>", methods=['GET', 'POST'])
def delete_bucketlist(id):
    if check_current_user() is True:
        global current_user

        bucketlist = classes.Bucketlist()
        bucketlist.delete_bucketlist(current_user[1], int(id))

        return redirect(url_for("user_bucket_lists"))

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>LLogin Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))


################# Bucketlist Activity functions
#
# View all Bucketlist Activities
#
@app.route("/bucketlist-activities-for/<bucketlist_id>")
def user_bucket_lists_activities(bucketlist_id):
    if check_current_user() is True:

        bucketlist_id = int(bucketlist_id)
        global current_user

        bucketlist_details = []
        activities = []

        # from bucketlists
        for key, value in all_bucketlists[current_user[1]][bucketlist_id].items():
            bucketlist_details.append(key)


        #check if user email has been set with bucketlist activites
        if current_user[1] in all_bucketlists_activities:

            # Get specific bucketlists
            for i in all_bucketlists_activities[current_user[1]]:
                for key, value in i.items():
                    if value[2] == bucketlist_details[0]:
                        activities.append(i)


            return render_template('view_bucket_list_activities.html',
                                   bucketlist_info=bucketlist_details,
                                   bucketlist_key=bucketlist_id,
                                   activities=activities)
        else:
            return render_template('view_bucket_list_activities.html',
                                   bucketlist_info=bucketlist_details,
                                   bucketlist_key=bucketlist_id)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>LLogin Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))

#
# Load Bucketlist Activity Page
#
@app.route("/add-bucketlist-activity/<bucketlist_id>/<bucketlist>")
def activity_page(bucketlist_id, bucketlist):

    if check_current_user() is True:

        form = ActivityForm()

        bucketlist_key = int(bucketlist_id)
        bucket = bucketlist
        global current_user


        return render_template('add_activity.html', form=form,
                               bucketlist_key=bucketlist_key,
                               bucketlist=bucket)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>LLogin Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))

#
# Create Bucketlist Activity Page
#
@app.route("/create-bucketlist-activity/<bucketlist_id>/<bucketlist>",  methods=['GET', 'POST'])
def create_activity(bucketlist_id, bucketlist):

    form = ActivityForm(request.form)

    bucketlist_key = int(bucketlist_id)
    bucket = bucketlist
    global current_user

    if form.validate_on_submit():
        activity = classes.Bucketlist_Activities()
        activity.create_bucketlist_activity(current_user[1], bucket,
                                            request.form.get("bucketlist_activity_name"),
                                            request.form.get("date"), False)

        success = Markup("<div class='alert alert-success' role='alert'>\
                        <strong>Done! </strong>Added "\
                        +request.form.get("bucketlist_activity_name")+"\
                        </div>")

        flash(success)

        #print(all_bucketlists_activities[current_user[1]])

        return redirect(url_for("user_bucket_lists_activities", bucketlist_id=bucketlist_key))

    else:

        return render_template('add_activity.html', form=form)

#
# Load Bucketlist Activity page
#
@app.route("/change-bucketlist-activity/<activity_id>/<bucketlist_id>/<bucketlist>")
def change_bucketlist_activity(activity_id, bucketlist_id, bucketlist):
    if check_current_user() is True:

        form = ActivityFormUpdate()

        activity_id = int(activity_id)
        bucketlist_id = int(bucketlist_id)
        bucket = bucketlist
        global current_user

        activiy_detail = all_bucketlists_activities[current_user[1]][activity_id]

        for key, value in activiy_detail.items():
            form.bucketlist_activity_name.data = key
            form.date.data = value[1]

        return render_template("change_activity.html", form=form, activity_id=activity_id,
                               bucketlist=bucket, bucketlist_id=bucketlist_id)

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>LLogin Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))

#
# Update Bucketlist Activity
#
@app.route("/update-bucketlist-activity/<activity_id>/<bucketlist_id>/<bucketlist>", methods=['GET', 'POST'])
def update_bucketlist_activity(activity_id, bucketlist_id, bucketlist):
    if check_current_user() is True:
        form = ActivityFormUpdate(request.form)
        global current_user

        bucketlist_activity_key = int(activity_id)
        bucketlist_id = int(bucketlist_id)
        bucket = bucketlist

        if form.validate_on_submit():
            user_bucketlist_activity = classes.Bucketlist_Activities()


            user_bucketlist_activity.update_bucketlist_activity(current_user[1],
                                                                bucketlist_activity_key,
                                                                bucket, request.form.get("date"),
                                                                request.form.get("bucketlist_activity_name"),
                                                                False)

            success = Markup("<div class='alert alert-success' role='alert'>\
                        <strong>Done! </strong>Updated "\
                        +request.form.get("bucketlist_activity_name")+"\
                        </div>")

            flash(success)


            return redirect(url_for("user_bucket_lists_activities", bucketlist_id=bucketlist_id))

        else:
            return render_template("change_activity.html", form=form, activity_id=activity_id, 
                                   bucketlist=bucket, bucketlist_id=bucketlist_id)
    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))


#
# Delete Bucketlist Activity
#
@app.route("/delete-bucketlist-activity/<activity_id>/<bucketlist_id>", methods=['GET', 'POST'])
def delete_bucketlist_activity(activity_id, bucketlist_id):
    if check_current_user() is True:
        global current_user
        bucketlist_activity_key = int(activity_id)
        bucketlist_id = int(bucketlist_id)

        remove_activity = classes.Bucketlist_Activities()
        remove_activity.delete_bucketlist_activity(current_user[1], bucketlist_activity_key)

        success = Markup("<div class='alert alert-success' role='alert'>\
                    <strong>Done! </strong>Bucketlist Removed</div>")

        flash(success)

        return redirect(url_for("user_bucket_lists_activities", bucketlist_id=bucketlist_id))


    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))


#
# Done with Bucketlist Activity
#
@app.route("/done-with-activity/<activity_id>/<bucketlist_id>/<bucketlist>/<done>")
def done_with_activity(activity_id, bucketlist_id, bucketlist, done):
    if check_current_user() is True:
        global current_user

        bucketlist_activity_key = int(activity_id)
        bucketlist_id = int(bucketlist_id)
        bucket = bucketlist

        print(all_bucketlists_activities[current_user[1]][bucketlist_activity_key])

        if int(done) == 1:
            bucketlist_activity_done = True
        else:
            bucketlist_activity_done = False

        activity_name = ""

        for key, value in \
         all_bucketlists_activities[current_user[1]][bucketlist_activity_key].items():
         
            value[0] = bucketlist_activity_done
            activity_name = key


        print(all_bucketlists_activities[current_user[1]][bucketlist_activity_key])

        success = Markup("<div class='alert alert-success' role='alert'>\
                    <strong>Done! </strong>Changed Activity status for "\
                    +activity_name+"\
                    </div>")

        flash(success)


        return redirect(url_for("user_bucket_lists_activities", bucketlist_id=bucketlist_id))

    else:
        error = Markup("<div class='alert alert-danger' role='alert'>\
                        <strong>Login Required! </strong>You must be logged in to\
                        to access that page\
                        </div>")

        flash(error)
        return redirect(url_for("login"))



@app.errorhandler(404)
def nage_not_found(error):
    return render_template('404.html'), 404




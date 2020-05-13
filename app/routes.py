from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user
from flask import current_app as app
from .models import db,User,Vote
from sqlalchemy import func



# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

def tally_votes():
    #sqlalchemy group by to tally all votes
    return db.session.query(Vote.candidate, func.count(Vote.candidate)).group_by(Vote.candidate).all()


@main_bp.route('/admin', methods=["GET"])
@login_required
def admin():
    if current_user.is_admin == 1:
	    return render_template('chart.html', data=tally_votes())
    flash("You are not the admin! Nice try.")
    return redirect(url_for('main_bp.logout'))


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Serve logged-in Dashboard."""
    return render_template('dashboard.jinja2',
                           title='Voting Dashboard',
                           template='dashboard-template',
                           current_user=current_user,
                           body="You are now logged in!")

@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    flash("Successfully Logged out.")
    return redirect(url_for('auth_bp.login'))

@main_bp.route("/vote", methods=["GET","POST"])
@login_required
def vote_page():
    """ Serve logged in user the option to vote """
    vote = request.args.get("votefor")
    print(current_user.name+" is trying to voting for "+vote)
    existing_voter = Vote.query.filter_by(user_id=current_user.id).first()
    if existing_voter is None:
        vote = Vote(candidate = vote, user_id=current_user.id)
        db.session.add(vote)
        db.session.commit()
        flash("Succesfully Voted")
        return redirect(url_for('main_bp.logout'))
    flash("You have already voted")
    return redirect(url_for('main_bp.logout'))
    
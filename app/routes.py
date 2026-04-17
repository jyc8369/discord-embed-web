import secrets
from flask import (
    current_app,
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash,
    abort,
)
from .discord_oauth import get_authorization_url, exchange_code, fetch_user_info
from .discord_client import DiscordClient, DiscordAPIError
from .services.embeds import (
    save_embed_record,
    get_user_records,
    get_record,
    delete_embed_record,
    update_embed_record,
)


def register_routes(app):
    @app.route("/")
    def index():
        user = session.get("discord_user")
        return render_template("index.html", user=user)

    @app.route("/login")
    def login():
        state = secrets.token_urlsafe(16)
        session["oauth_state"] = state
        authorization_url = get_authorization_url(state)
        return redirect(authorization_url)

    @app.route("/callback")
    def callback():
        if request.args.get("state") != session.pop("oauth_state", None):
            abort(400, "Invalid OAuth state")

        code = request.args.get("code")
        if not code:
            flash("Discord authorization failed.", "danger")
            return redirect(url_for("index"))

        token_data = exchange_code(code)
        user_info = fetch_user_info(token_data["access_token"])
        session["discord_user"] = {
            "id": user_info["id"],
            "username": user_info["username"],
            "discriminator": user_info.get("discriminator"),
        }
        flash(f"Logged in as {user_info['username']}#{user_info.get('discriminator')}", "success")
        return redirect(url_for("index"))

    @app.route("/logout")
    def logout():
        session.pop("discord_user", None)
        flash("Logged out successfully.", "info")
        return redirect(url_for("index"))

    def build_embed_payload(form):
        title = form.get("title", "").strip()
        description = form.get("description", "").strip()
        color_value = form.get("color", "").strip().lstrip("#")
        footer_text = form.get("footer_text", "").strip()
        image_url = form.get("image_url", "").strip()
        thumbnail_url = form.get("thumbnail_url", "").strip()
        fields = []

        for i in range(1, 4):
            name = form.get(f"field_{i}_name", "").strip()
            value = form.get(f"field_{i}_value", "").strip()
            if name and value:
                fields.append({"name": name, "value": value, "inline": False})

        embed = {}
        if title:
            embed["title"] = title
        if description:
            embed["description"] = description
        if color_value:
            try:
                embed["color"] = int(color_value, 16)
            except ValueError:
                pass
        if footer_text:
            embed["footer"] = {"text": footer_text}
        if image_url:
            embed["image"] = {"url": image_url}
        if thumbnail_url:
            embed["thumbnail"] = {"url": thumbnail_url}
        if fields:
            embed["fields"] = fields

        return embed

    def require_login():
        user = session.get("discord_user")
        if not user:
            flash("Please log in with Discord first.", "warning")
            return None
        return user

    @app.route("/embed/create", methods=["POST"])
    def create_embed():
        user = require_login()
        if user is None:
            return redirect(url_for("index"))

        embed_payload = build_embed_payload(request.form)
        if not embed_payload:
            flash("Embed content is required.", "warning")
            return redirect(url_for("index"))

        discord_client = DiscordClient()
        try:
            result = discord_client.send_embed(
                current_app.config["DISCORD_CHANNEL_ID"], embed_payload
            )
        except DiscordAPIError as exc:
            current_app.logger.error("Discord send failed: %s", exc)
            flash("Unable to send embed to Discord.", "danger")
            return redirect(url_for("index"))

        save_embed_record(user, embed_payload, result["id"], result["channel_id"])
        flash("Embed sent and saved to history.", "success")
        return redirect(url_for("history"))

    @app.route("/history")
    def history():
        user = require_login()
        if user is None:
            return redirect(url_for("index"))

        records = get_user_records(user["id"])
        return render_template("history.html", user=user, records=records)

    @app.route("/history/<int:record_id>/edit")
    def edit_history(record_id):
        user = require_login()
        if user is None:
            return redirect(url_for("index"))

        record = get_record(record_id)
        if record is None or record.user_id != user["id"]:
            abort(404)

        return render_template("edit.html", user=user, record=record)

    @app.route("/history/<int:record_id>/update", methods=["POST"])
    def update_history(record_id):
        user = require_login()
        if user is None:
            return redirect(url_for("index"))

        record = get_record(record_id)
        if record is None or record.user_id != user["id"]:
            abort(404)

        embed_payload = build_embed_payload(request.form)
        if not embed_payload:
            flash("Embed content cannot be empty.", "warning")
            return redirect(url_for("edit_history", record_id=record_id))

        discord_client = DiscordClient()
        try:
            discord_client.update_embed(record.channel_id, record.message_id, embed_payload)
            update_embed_record(record, embed_payload)
        except DiscordAPIError as exc:
            current_app.logger.error("Discord update failed: %s", exc)
            flash("Unable to update embed on Discord.", "danger")
            return redirect(url_for("edit_history", record_id=record_id))

        flash("Embed record updated successfully.", "success")
        return redirect(url_for("history"))

    @app.route("/history/<int:record_id>/delete", methods=["POST"])
    def delete_history(record_id):
        user = require_login()
        if user is None:
            return redirect(url_for("index"))

        record = get_record(record_id)
        if record is None or record.user_id != user["id"]:
            abort(404)

        discord_client = DiscordClient()
        try:
            discord_client.delete_message(record.channel_id, record.message_id)
        except DiscordAPIError as exc:
            current_app.logger.warning("Discord delete failed: %s", exc)

        delete_embed_record(record)
        flash("Embed history record deleted.", "success")
        return redirect(url_for("history"))

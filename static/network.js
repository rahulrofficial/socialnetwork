document.addEventListener("DOMContentLoaded", function (event) {
	if (document.getElementById("profile_div")) {
		if (document.querySelector("#unfollow_btn")) {
			document
				.querySelector("#unfollow_btn")
				.addEventListener("click", (event) => {
					follow_unfollow(event, "unfollow");
				});
		}

		if (document.getElementById("follow_btn"))         
        {
			document
				.getElementById("follow_btn")
				.addEventListener("click", (event) => {
					follow_unfollow(event, "follow");
				});
		}
        document
			.querySelector("#profile_edit_btn")
			.addEventListener("click", () => {
				document.querySelector("#profile_edit_form").style.display = "block";
				document.querySelector("#details_display").style.display = "none";
			});
		document
			.querySelector("#profile_submit_btn")
			.addEventListener("click", () => {
				document.querySelector("#profile_edit_form").style.display = "none";
				document.querySelector("#details_display").style.display = "block";
			});
		//
	}
	if (
		document.getElementById("index_div") ||
		document.getElementById("profile_div") ||
		document.getElementById("view_post_div") ||
		document.getElementById("following_div") ||
        document.getElementById("liked_post_div")
	) {
		if (document.querySelectorAll(".view_btn")) {
			document.querySelectorAll(".view_btn").forEach((btn) => {
				btn.addEventListener("click", (event) => {
					view = event.target;

					window.location.replace(`/view_post/${view.dataset.post_id}`);
				});
			});
		}

		if (document.querySelectorAll(".delete_btn")) {
			document.querySelectorAll(".delete_btn").forEach((btn) => {
				btn.addEventListener("click", (event) => {
					post_manipulation(event, "delete");
				});
			});
		}

		if (document.querySelectorAll(".edit_btn")) {
			document.querySelectorAll(".edit_btn").forEach((btn) => {
				btn.addEventListener("click", (event) => {
					var post_id = event.target.dataset.post_id;
					var submit = document.getElementById(`index_submit_btn_${post_id}`);

					var delete_btn = document.getElementById(
						`index_delete_btn_${post_id}`
					);
					event.target.style.display = "none";

					delete_btn.style.display = "none";
					submit.style.display = "block";
					post_manipulation(event, "edit");
				});
			});
		}

		if (document.querySelectorAll(".like_btn")) {
			document.querySelectorAll(".like_btn").forEach((btn) => {
				btn.addEventListener("click", (event) => {
					post_manipulation(event, "like");
				});
			});
		}
	}
});

function follow_unfollow(event, action) {
	profile_id = parseInt(event.target.dataset.profile_id);
	if (action == "follow") {
		fetch(`/follow_unfollow/${profile_id}`, {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				follow: true,
			}),
		}).then((response) => {
			if (response.status == 200) {
				window.location.replace(`/profile/${profile_id}`);
			}
		});
	} else if (action == "unfollow") {
		fetch(`/follow_unfollow/${profile_id}`, {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				follow: false,
			}),
		}).then((response) => {
			if (response.status == 200) {
				window.location.replace(`/profile/${profile_id}`);
			}
		});
	}
}

function post_manipulation(event, action) {
	post_id = parseInt(event.target.dataset.post_id);

	if (action == "edit") {
		var submit = document.getElementById(`index_submit_btn_${post_id}`);
		var delete_btn = document.getElementById(`index_delete_btn_${post_id}`);
		var edit_btn = document.getElementById(`index_edit_btn_${post_id}`);

		fetch(`/post_data/${post_id}`)
			.then((response) => response.json())
			.then((post) => {
				var content_div = document.getElementById(
					`index_content_div_${post_id}`
				);
				content_div.innerHTML = `<textarea class='form-control mt-2' id='editedtext'>${post.content}</textarea>`;
				submit.addEventListener("click", (submit_event) => {
					var edited_text = document.getElementById("editedtext").value;
					fetch(`/post_manipulation/${post_id}`, {
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify({
							content: edited_text,
							action: "edit",
						}),
					})
						.then((response) => response.json())
						.then((data) => {
							if (data.status == 200) {
								fetch(`/post_data/${post_id}`, { method: "GET" })
									.then((post_response) => post_response.json())
									.then((post) => {
										content_div.innerHTML = `<h6 class="mt-2">${post.content}</h6>`;
										edit_btn.style.display = "block";
										delete_btn.style.display = "block";
										submit.style.display = "none";
									});
							}
						});
				});
			});
	}
	if (action == "delete") {
		var display_div = document.getElementById(`display_div_${post_id}`);

		fetch(`/post_manipulation/${post_id}`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				action: "delete",
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.status == 200) {
					display_div.style.display = "none";
				}
			});
	}

	if (action == "like") {
		fetch(`/like_unlike/${post_id}`, {
			method: "PUT",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				like: true,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.status == 200) {
					fetch(`/post_data/${post_id}`, { method: "GET" })
						.then((post_response) => post_response.json())
						.then((post) => {
							button = document.getElementById(`index_like_btn_${post_id}`);
							button.innerHTML = `<i data-post_id="${post_id}" style="font-size: 24px; color: red" class="fa">&#xf004;</i>
                                ${post.likes} Likes`;
						});
				}
			});
	}
}

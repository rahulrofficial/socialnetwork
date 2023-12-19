document.addEventListener("DOMContentLoaded", function (event) {
	display_tabs("all", event);
	document.querySelector("#allpost").addEventListener("click", (event) => {
		display_tabs("all", event);
	});
	document.querySelector("#network").addEventListener("click", (event) => {
		display_tabs("all", event);
	});
	document.querySelector("#follow").addEventListener("click", (event) => {
		display_tabs("following", event);
	});

	document.querySelector("#newpost").addEventListener("click", (event) => {
		display_tabs("newpost", event);
	});

	document.querySelector("#username").addEventListener("click", (event) => {
		display_tabs("profile", event);
	});
	if (document.querySelector("#button_follow")) {
		document
			.querySelector("#button_follow")
			.addEventListener("click", (event) => {});
	}

	document.querySelector("#compose-form").onsubmit = (event) => {
		const form_element = document.querySelector("#compose-form");

		const body = document.querySelector("#compose-body");

		fetch(`/posts/post`, {
			method: "POST",
			body: JSON.stringify({
				content: body.value,
			}),
		}).then((response) => {
			if (response.status == 201) {
				body.value = "";
				display_tabs("all");
			}
		});

		return false;
	};
});

function compose() {
	// Clear out composition fields

	document.querySelector("#compose-body").value = "";
}
var prof_id = 1;

function display_tabs(tab, event = null, page = 1) {
	if (tab === "all") {
		document.querySelector("#post-view").innerHTML = "";
		document.querySelector("#post-view").style.display = "block";
		document.querySelector("#pagination_view").style.display = "block";
		if (document.querySelector("#compose-view")) {
			document.querySelector("#compose-view").style.display = "block";
		}

		document.querySelector("#profile-view").style.display = "none";
		document.querySelector("#post-view").innerHTML = "";
		const heading = document.createElement("h3");
		heading.innerHTML = "All Posts";
		heading.className = "ml-3";
		document.querySelector("#post-view").append(heading);
		fetch(`/postbox/all/username/${page}`)
			.then((response) => response.json())
			.then((posts) => {
				if (posts.posts.length != 0) {
					posts.posts.forEach((element) => {
						const div = document.createElement("div");
						const a = document.createElement("a");

						div.className = "border border-dark m-3 p-2 w-75 rounded";
						a.innerHTML = `<span style='color:grey;font-size:15px;'>Posted by:</span> ${element.owner.username}`;
						a.style.color = "blue";
						a.style.fontWeight = "bold";
						a.dataset.prof_id = element.owner.id;
						a.addEventListener("click", (event) => {
							display_tabs("profile", event);
						});
						const h4 = document.createElement("h5");
						const h6 = document.createElement("h6");
						const p = document.createElement("p");

						const br = document.createElement("br");
						const button_link = document.createElement("button");
						button_link.className = "btn btn-outline-danger disabled";
						button_link.ariaDisabled = "true";
						button_link.innerHTML = `<i style="font-size:24px;color:red;" class="fa">&#xf004;</i> ${element.likes} Likes`;
						button_link.dataset.id = element.id;
						button_link.id = `button_post${element.id}`;
						button_link.dataset.page = posts.page_num;
						if (posts.is_signin) {
							button_link.className = "btn btn-outline-danger ";
							button_link.ariaDisabled = "false";
							button_link.addEventListener("click", (event) => {
								like_unlike(event, tab);
							});
						}

						const edit = document.createElement("button");
						edit.className = "badge badge-primary";
						edit.dataset.id = element.id;
						edit.innerHTML = "Edit";
						edit.addEventListener("click", (event) => {
							display_tabs("edit", event);
						});
						h4.append(a);
						h6.innerHTML = element.content;
						h6.className = "mt-2";
						h6.id = `post${element.id}`;
						p.innerHTML = `<span style='color:grey;'>${element.timestamp}</span>`;
						div.append(h4);
						if (posts.is_signin) {
							if (element.owner.username == posts.username) {
								div.append(br);
								div.append(edit);
								div.append(br);
							}
						}

						div.append(h6);
						div.append(p);
						div.append(button_link);
						document.querySelector("#post-view").append(div);
					});
					document.querySelector("#pagination_view").innerHTML = "";

					pagination(
						tab,
						(total = posts.total_pages),
						(has_prev = posts.has_previous),
						(first = 1),
						(previous = posts.previous_page_no),
						(current = posts.page_num),
						(has_nxt = posts.has_next),
						(next = posts.next_page_number)
					);
				} else {
					document.querySelector("#pagination_view").innerHTML = "";
					const h4 = document.createElement("h4");
					h4.className = "ml-3";
					h4.innerHTML = `No posts yet...`;
					document.querySelector("#post-view").append(h4);
				}
			});
	}
	if (tab == "following") {
		document.querySelector("#post-view").innerHTML = "";
		document.querySelector("#pagination_view").style.display = "block";
		document.querySelector("#compose-view").style.display = "none";
		document.querySelector("#profile-view").style.display = "none";
		document.querySelector("#post-view").style.display = "block";
		const heading = document.createElement("h3");
		heading.className = "ml-3";
		heading.innerHTML = "Following";
		document.querySelector("#post-view").append(heading);
		fetch(`/postbox/following/username/${page}`)
			.then((response) => response.json())
			.then((posts) => {
				if (posts.posts.length != 0) {
					posts.posts.forEach((element) => {
						const div = document.createElement("div");
						const a = document.createElement("a");
						div.className = "border border-dark m-3 p-2 w-75 rounded";
						a.innerHTML = `<span style='color:grey;font-size:15px;'>Posted by:</span> ${element.owner.username}`;
						a.dataset.prof_id = element.owner.id;
						a.style.color = "blue";
						a.style.fontWeight = "bold";
						a.addEventListener("click", (event) => {
							display_tabs("profile", event);
						});
						const h4 = document.createElement("h5");
						const h6 = document.createElement("h6");
						const p = document.createElement("p");
						const br = document.createElement("br");
						const button_link = document.createElement("button");
						button_link.className = "btn btn-outline-danger disabled";
						button_link.innerHTML = `<i style="font-size:24px;color:red;" class="fa">&#xf004;</i> ${element.likes} Likes`;
						button_link.dataset.id = element.id;
						button_link.id = `button_post${element.id}`;
						button_link.dataset.page = posts.page_num;
						if (posts.is_signin) {
							button_link.className = "btn btn-outline-danger ";

							button_link.addEventListener("click", (event) => {
								like_unlike(event, tab);
							});
						}

						h4.append(a);
						h6.innerHTML = element.content;
						p.innerHTML = `<span style='color:grey;'>${element.timestamp}</span>`;
						div.append(h4);

						div.append(h6);
						div.append(p);
						div.append(button_link);
						document.querySelector("#post-view").append(div);
					});
					document.querySelector("#pagination_view").innerHTML = "";

					pagination(
						tab,
						(total = posts.total_pages),
						(has_prev = posts.has_previous),
						(first = 1),
						(previous = posts.previous_page_no),
						(current = posts.page_num),
						(has_nxt = posts.has_next),
						(next = posts.next_page_number)
					);
				} else {
					document.querySelector("#pagination_view").innerHTML = "";
					const h4 = document.createElement("h4");
					h4.className = "ml-3";
					h4.innerHTML = `Hasn't followed anyone yet...`;
					document.querySelector("#post-view").append(h4);
				}
			});
	}
	if (tab == "newpost") {
		document.querySelector("#post-view").style.display = "none";
		document.querySelector("#profile-view").style.display = "none";
		document.querySelector("#pagination_view").style.display = "none";
		document.querySelector("#compose-view").style.display = "block";
	}

	if (tab == "profile") {
		document.querySelector("#profile-view").innerHTML = "";
		const parent_div = document.createElement("div");
		const child1_div = document.createElement("div");
		const child2_div = document.createElement("div");
		parent_div.style.margin = "10px";
		parent_div.style.padding = "5px";

		document.querySelector("#post-view").innerHTML = "";
		if (document.querySelector("#compose-view")) {
			document.querySelector("#compose-view").style.display = "none";
		}
		document.querySelector("#profile-view").style.display = "block";

		if (event.target.dataset.prof_id) {
			prof_id = event.target.dataset.prof_id;
		} else {
			id = prof_id;
		}

		const name = document.createElement("h2");
		name.id = "username_display";
		fetch(`/profile/${prof_id}`)
			.then((response) => response.json())
			.then((posts) => {
				const followers = document.createElement("h5");
				const following = document.createElement("h3");
				const follow_div = document.createElement("div");

				const span = document.createElement("span");
				span.className = "badge bg-secondary ml-3";
				span.innerHTML = "following";
				const follow_button = document.createElement("button");
				follow_button.className = "badge bg-success ml-3";
				follow_button.dataset.id = prof_id;
				follow_button.innerHTML = "follow";
				follow_button.addEventListener("click", (event) => {
					follow_unfollow("follow", event);
				});
				const unfollow_button = document.createElement("button");
				unfollow_button.className = "badge bg-danger ml-2";
				unfollow_button.dataset.id = prof_id;
				unfollow_button.innerHTML = "unfollow";
				unfollow_button.addEventListener("click", (event) => {
					follow_unfollow("unfollow", event);
				});

				if (!posts.is_owner) {
					if (posts.is_follower) {
						follow_div.append(span);

						follow_div.append(unfollow_button);
					} else {
						follow_div.append(follow_button);
					}
				}

				//follow_div.innerHTML =`<span id="following_badge" class="badge bg-secondary">${_following}</span><button id="button_follow" type="button" class="badge bg-success">${follow}</button> <button id="button_unfollow" type="button" class="badge bg-danger">${unfollow}</button>`

				name.innerHTML = `${posts.user.username}`;
				name.className = "ml-3";
				following.innerHTML = `Posts`;
				following.className = "ml-3";
				followers.className = "ml-3";
				followers.innerHTML = `</br><strong>${posts.following}</strong> <i>following </i>         <strong>${posts.followers}</strong> <i>followers</i><hr> `;
				child1_div.append(name);
				child1_div.append(follow_div);
				child1_div.append(followers);
				child1_div.append(following);
				document.querySelector("#profile-view").append(child1_div);
				fetch(`/postbox/profile/${posts.user.username}/${page}`)
					.then((response) => response.json())
					.then((prof_post) => {
						prof_post.posts.forEach((element) => {
							const div = document.createElement("div");
							div.className = "border border-dark m-3 p-2 w-75 rounded";
							const br = document.createElement("br");
							const button_link = document.createElement("button");
							button_link.className = "btn btn-outline-danger disabled";
							button_link.innerHTML = `<i style="font-size:24px;color:red;" class="fa">&#xf004;</i> ${element.likes} Likes`;
							button_link.dataset.id = element.id;
							button_link.id = `button_post${element.id}`;
							button_link.dataset.page = prof_post.page_num;
							button_link.dataset.prof_id = prof_id;

							if (prof_post.is_signin) {
								button_link.className = "btn btn-outline-danger ";

								button_link.addEventListener("click", (event) => {
									like_unlike(event, tab);
								});
							}
							div.style.margin = "10px";
							div.style.padding = "5px";
							div.style.borderStyle = "solid";
							const h3 = document.createElement("p");
							h3.style.fontSize = "20px";
							h3.innerHTML = `${element.content}`;
							const p = document.createElement("p");
							p.innerHTML = `<span style='color:grey;'>${element.timestamp}</span>`;
							div.append(h3);
							div.append(p);
							div.append(button_link);
							document.querySelector("#post-view").append(div);
						});
						document.querySelector("#pagination_view").innerHTML = "";
						if (prof_post.posts.length != 0) {
							pagination(
								tab,
								(total = prof_post.total_pages),
								(has_prev = prof_post.has_previous),
								(first = 1),
								(previous = prof_post.previous_page_no),
								(current = prof_post.page_num),
								(has_nxt = prof_post.has_next),
								(next = prof_post.next_page_number)
							);
						}
					});
			});
	}

	if (tab == "edit") {
		fetch(`/post/${event.target.dataset.id}`, { method: "GET" })
			.then((response) => response.json())
			.then((post) => {
				post_id = event.target.dataset.id;
				const body = document.querySelector(`#post${post_id}`);
				body.innerHTML = `<textarea class='form-control mt-2' id='editedtext'>${post.content}</textarea></br><button class="btn btn-info btn-sm" id='savepost'>Save</button>`;

				document
					.querySelector("#savepost")
					.addEventListener("click", (event) => {
						const text = document.querySelector("#editedtext").value;
						fetch(`/posts/edit`, {
							method: "POST",
							body: JSON.stringify({
								content: text,
								id: post_id,
							}),
						}).then((response) => {
							if (response.status == 201) {
								fetch(`/post/${post_id}`, { method: "GET" })
									.then((response) => response.json())
									.then((post) => {
										body.innerHTML = `<h6>${post.content}</h6>`;
									});
							}
						});
					});
			});
	}
}

function follow_unfollow(tab, event) {
	if (tab == "follow") {
		fetch(`/profile/${event.target.dataset.id}`, {
			method: "PUT",
			body: JSON.stringify({
				follow: true,
			}),
		}).then((response) => {
			display_tabs("following", event);
		});
	}
	if (tab == "unfollow") {
		fetch(`/profile/${event.target.dataset.id}`, {
			method: "PUT",
			body: JSON.stringify({
				follow: false,
			}),
		}).then((response) => {
			display_tabs("following", event);
		});
	}
}

function like_unlike(event, tab) {
	let post_id = event.target.dataset.id;
	fetch(`/post/${post_id}`, {
		method: "PUT",
	}).then((response) => {
		if (response.status == 201) {
			fetch(`/post/${post_id}`, { method: "GET" })
				.then((response) => response.json())
				.then((post) => {
					like_button = document.querySelector(`#button_post${post_id}`);
					like_button.innerHTML = `<i style="font-size:24px;color:red;" class="fa">&#xf004;</i> ${post.likes} Likes`;
				});
		}
	});
}

function pagination(
	tab,
	total,
	has_prev,
	first,
	previous,
	current,
	has_nxt,
	next
) {
	document.querySelector("#pagination_view").innerHTML = "";

	const nav = document.createElement("nav");
	const ul = document.createElement("ul");
	ul.className = "pagination";
	const li_first = document.createElement("li");
	li_first.className = "page-item";
	const button_first = document.createElement("button");
	button_first.className = "page-link";
	button_first.id = "first";
	button_first.innerHTML = "First";
	li_first.addEventListener("click", (event) => {
		display_tabs(tab, event, first);
	});
	li_first.append(button_first);

	const li_previous = document.createElement("li");
	li_previous.className = "page-item";
	const button_previous = document.createElement("button");
	button_previous.className = "page-link";
	button_previous.id = "previous";
	button_previous.innerHTML = "Previous";
	li_previous.addEventListener("click", (event) => {
		display_tabs(tab, event, previous);
	});
	li_previous.append(button_previous);

	const li_current = document.createElement("li");
	li_current.className = "page-item";
	const button_current = document.createElement("button");
	button_current.className = "page-link";
	button_current.id = "current_page";
	button_current.innerHTML = `Page ${current} of ${total}`;
	li_current.addEventListener("click", (event) => {
		display_tabs(tab, event, current);
	});
	li_current.append(button_current);

	const li_next = document.createElement("li");
	li_next.className = "page-item";
	const button_next = document.createElement("button");
	button_next.className = "page-link";
	button_next.id = "next";
	button_next.innerHTML = "Next";

	li_next.addEventListener("click", (event) => {
		display_tabs(tab, event, next);
	});
	li_next.append(button_next);

	const li_last = document.createElement("li");
	li_last.className = "page-item";
	const button_last = document.createElement("button");
	button_last.className = "page-link";
	button_last.id = "last";
	button_last.innerHTML = "Last";
	li_last.addEventListener("click", (event) => {
		display_tabs(tab, event, total);
	});
	li_last.append(button_last);
	if (has_prev) {
		ul.append(li_first);
		ul.append(li_previous);
	}

	ul.append(li_current);

	if (has_nxt) {
		ul.append(li_next);
		ul.append(li_last);
	}

	nav.append(ul);

	document.querySelector("#pagination_view").append(nav);
}

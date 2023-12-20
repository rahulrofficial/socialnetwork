document.addEventListener("DOMContentLoaded", function (event) {


if (document.getElementById("profile_div"))
{
    if(document.querySelector("#unfollow_btn")){
        document.querySelector("#unfollow_btn").addEventListener('click',(event)=>{
            follow_unfollow(event,"unfollow")
        });
    }
    

    if(document.getElementById("follow_btn")){
        document.getElementById("follow_btn").addEventListener('click',(event)=>{
            follow_unfollow(event,"follow")
        });
    }
    

}







});

function follow_unfollow(event,action){
    profile_id =parseInt( event.target.dataset.profile_id);
    if (action=="follow"){

        fetch(`/follow_unfollow/${profile_id}`, {
			method: "PUT",
			body: JSON.stringify({
				follow: true,
			}),
		}).then((response) => {
            console.log(response);
			
		});

    }
    else if (action=="unfollow"){
        fetch(`/follow_unfollow/${profile_id}`, {
			method: "PUT",
			body: JSON.stringify({
				follow: false,
			}),
		}).then((response) => {
			console.log(response);
            
		});


    }
}
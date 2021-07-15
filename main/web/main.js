function execute(){
	var keyword,request_date,quantity,category,way_to_download;
	keyword=document.getElementById("keyword_input").value;
	request_date=document.getElementById("date").value;
	quantity=document.getElementById("quantity_input").value;
	category=document.getElementsByName("category_input");
	for(var temp=0;temp<document.getElementsByName("category_input").length;temp++){
		if(category[temp].checked){
			category=category[temp].value;
			break;
		}
	}
	way_to_download=document.getElementsByName("method_input");
	for(var temp=0;temp<document.getElementsByName("method_input").length;temp++){
		if(way_to_download[temp].checked){
			way_to_download=way_to_download[temp].value;
			break;
		}
	}
	if(request_date=="" && document.getElementsByName("time_on_or_off").value=="on"){
		alert("date filter is required");
	}
	else{
		document.getElementById("btn").disabled=true;
		document.getElementById("story").value="crawling......\n";
		eel.main(keyword,request_date,quantity,category,way_to_download);
		}
	
}

eel.expose(show_percentage);
function show_percentage(num){
	document.getElementById("btn").disabled=true;
	document.getElementById("percent").textContent=num+"%";
	document.getElementById("progress").value=num;
}
eel.expose(show_output);
function show_output(word){
	var story=document.getElementById("story");
	story.scrollTop=story.scrollHeight;
	story.value+=word;
}
function open_time_filter(){
	
	document.getElementById("date").disabled=false;
	document.getElementsByName("time_on_or_off").value="on"
}
function close_time_filter(){
	
	document.getElementById("date").disabled=true;
	document.getElementsByName("time_on_or_off").value="off"
}


function hide_output(){
	if(document.getElementById("story").style.display==""){
		document.getElementById("story").style.display="none";
	}
	else if(document.getElementById("story").style.display=="none"){
		document.getElementById("story").style.display="inline";
	}
	else{
		document.getElementById("story").style.display="none";
	}
	
}


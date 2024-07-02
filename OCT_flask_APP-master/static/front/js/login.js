var LoginHandler = function() {}

LoginHandler.prototype.listenSubmitEvent = function(){
    //一定记得按钮是一个带有 id 的元素（比如 <button id="submit-btn">Submit</button>），应该使用 # 来选择它
    $("#submit-btn").on("click", function(event){
        event.preventDefault();
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();
        //prop主要用于处理那些有实际的 boolean 值或者原生属性的 HTML 元素
        var remember = $("input[name='remember']").prop("checked");
        zlajax.post({
            url:"/login",
            data: {
                email,
                password,
                remember: remember?1:0
            },
            success: function (result) {
                if(result['code'] == 200){
                    var token = result['data']['token'];
                    var user = result['data']['user'];
                    localStorage.setItem("JWT_TOKEN_KEY", token);
                    localStorage.setItem("USER_KEY", JSON.stringify(user));
                    window.location = '/'
                }else
                {
                    alert(result['message']);
                }
            }
        })
        });
}

LoginHandler.prototype.run = function(){
    this.listenSubmitEvent();
}

$(function () {
    var handler = new LoginHandler();
    handler.run();
})
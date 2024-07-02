var RegisterHandler = function(){


}

RegisterHandler.prototype.listenSendCaptchaEvent = function ()  {
    var callback = function (event){
        //将js的原生对象：this 变为 jQuery对象
        var $this = $(this)  // 如果这个 callback 函数被用作某个按钮点击事件的处理函数，this 就指向那个按钮的 DOM 元素。
        //阻止默认的点击事件
        event.preventDefault();
        var email = $("input[name='email']").val() // 获取邮箱号

        var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;

        if(!email || !reg.test(email)){
            alert("请输入正确格式的邮箱！");
            return;
        }
        zlajax.get(
            {
                url:"/email/captcha?email=" + email,
                success: function (result){
                    if (result['code'] ==  200)
                    {
                        console.log("发送成功");
                        //取消按钮点击事件
                        $this.off("click");
                        //添加禁用状态
                        $this.attr("disabled",'disabled');
                        //开始倒计时
                        var countdown = 6;
                        var interval = setInterval(function (){
                            if(countdown>0){
                                $this.text(countdown);
                            }else
                            {
                                $this.text("发送验证码");
                                $this.attr("disabled",false );
                                $this.on("click",callback);//重新绑定callback
                                clearInterval(interval); //清理定时器
                            }
                            countdown--;
                        },1000)
                    }else{
                        var message = result['message'];
                        alert(message);
                    }

                }
            }
        )
    }
    $('#email-captcha-btn').on("click",callback);//寻找id为email-captcha-btn的按钮并监听点击事件
}

RegisterHandler.prototype.listenGraphCaptchaEvent = function(){
    $("#captcha-img").on("click",function (){
        console.log("点击验证码！")
        var $this = $(this);
        var src = $this.attr("src");
        //设置新的src
        let new_src = zlparam.setParam(src,"sign",Math.random())
        $this.attr("src",new_src);

    });
}

RegisterHandler.prototype.listenSubmitEvent = function(){
    $("#submit-btn").on("click",function (event){
        event.preventDefault();
        var email = $("input[name='email']").val();
        var email_captcha = $("input[name='email-captcha']").val();
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        var repeat_password = $("input[name='repeat-password']").val();
        var graph_captcha = $("input[name='graph-captcha']").val();


        zlajax.post({
            url:"/register",
            //data中的名字一定要与class RegisterForm(Form)中的名字相同
            data:{
                email,
                email_captcha,
                username,
                password, // 相同于 'password':password
                repeat_password,
                graph_captcha
            },
            success: function(result)
            {
                if(result['code'] == 200)
                {
                    window.location = '/login';
                }else{
                    alert(result['message']);
                }
            }
        })
    })
}


RegisterHandler.prototype.run = function(){
    this.listenSendCaptchaEvent();
    this.listenGraphCaptchaEvent();
    this.listenSubmitEvent();
}


//整个网页全加载后才能用
$(function(){
    var handler = new RegisterHandler();
    handler.run();

})
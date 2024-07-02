var SettingHandler = function () {
}

SettingHandler.prototype.listenAvatarUpload = function (){
    $("#avatar-input").on("change", function(){
        //当文件选择框的内容改变时，this.files[0]将获取用户选择的第一个文件（通常是图片）
    var image = this.files[0];
        //这使得可以通过AJAX发送二进制文件数据。formData.append("image", image);将选定的图片添加到表单数据中，键名为"image"。
    var formData = new FormData();
    formData.append("image", image);
    zlajax.post({
        url: "/avatar/upload",
        data: formData,
        //如果使用jquery上传文件则需要指定以下两个参数
        processData: false,
        contentType: false,
        success:function(result){
            if(result['code'] == 200){
                // console.log(result);
                var avatar = result['data']['avatar'];
                // console.log(avatar);
                var avatar_url = "/media/avatar/" + avatar;
                $('#avatar-img').attr("src", avatar_url)
            }
        }
    })
});
}


SettingHandler.prototype.run = function()
{
    this.listenAvatarUpload();

}

$(function () {
   var handler = new SettingHandler();
   handler.run();
})
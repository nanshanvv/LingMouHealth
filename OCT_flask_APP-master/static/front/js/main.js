$(document).ready(function () {
    // 初始化
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // 上传预览
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    // 显示上传的图像预览
    $('#imageUpload').change(function () {
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = new Image();
            img.src = e.target.result;
            img.onload = function () {
                var imgWidth = img.width;
                var imgHeight = img.height;

                // 动态调整预览区域的大小
                $('.img-preview').css({
                    'width': imgWidth + 'px',
                    'height': imgHeight + 'px'
                });

                // 显示预览图像
                $('#imagePreview').html('<img src="' + e.target.result + '" alt="Preview Image">');
                $('.image-section').show();
            }
        }
        reader.readAsDataURL(this.files[0]);
    });

    // 当上传文件时显示预览和预测按钮
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // 获取CSRF令牌
    var csrftoken = $('meta[name="csrf-token"]').attr('content');

    // 预测按钮点击事件
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        form_data.append('csrf_token', csrftoken);

        // 隐藏预测按钮，显示加载动画
        $(this).hide();
        $('.loader').show();

        // 发起预测请求
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            beforeSend: function(xhr) {
                // 设置CSRF令牌
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                // 显示结果并隐藏加载动画
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html('<p>Result: ' + data.result + '</p><p>Details: ' + data.details.replace(/\n/g, '<br>') + '</p>');
                $('#disclaimer').fadeIn(600);
                // console.log(data)
                // console.log(data.result);
                // console.log(data.detail)
                console.log('Success!');
            },
            error: function () {
                // 如果请求失败，隐藏加载动画并重新显示预测按钮
                $('.loader').hide();
                $('#btn-predict').show();
                console.log('Error!');
            }
        });
    });
});

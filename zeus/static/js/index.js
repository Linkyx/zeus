/**
 * Created by linky on 2017/5/1.
 */
$(function(){
    console.log("21312321312")
    // 初始化用户表单
    $('#participant-project').select2({
        tags: true,
        placeholder: "请选择用户",
    })

    var select2_data = [];
    $.ajax({
        url: '/get_all_user/', //远程数据地址
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            select2_data = data['message'];
            //初始化通知群组的下拉框
            $('#participant-project').select2({
                placeholder: '请选择选项',
                allowClear: true,
                tags: true,
                cache: false,
                data: select2_data  //数据
            });
        }
    })

    // 上传项目封面时实现预览效果
    $('#f').on('change', change);

    function change() {
    var pic = document.getElementById("preview"),
        file = document.getElementById("f");

    var ext=file.value.substring(file.value.lastIndexOf(".")+1).toLowerCase();

     // gif在IE浏览器暂时无法显示
     if(ext!='png'&&ext!='jpg'&&ext!='jpeg'){
         layer.msg("图片的格式必须为png或者jpg或者jpeg格式！", {icon: 5});
         return;
     }
     var isIE = navigator.userAgent.match(/MSIE/)!= null,
         isIE6 = navigator.userAgent.match(/MSIE 6.0/)!= null;

     if(isIE) {
        file.select();
        var reallocalpath = document.selection.createRange().text;

        // IE6浏览器设置img的src为本地路径可以直接显示图片
         if (isIE6) {
            pic.src = reallocalpath;
         }else {
            // 非IE6版本的IE由于安全问题直接设置img的src无法显示本地图片，但是可以通过滤镜来实现
             pic.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='image',src=\"" + reallocalpath + "\")";
             // 设置img的src为base64编码的透明图片 取消显示浏览器默认图片
             pic.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
         }
     }else {
        html5Reader(file);
     }
}

 function html5Reader(file){
     var file = file.files[0];
     var reader = new FileReader();
     reader.readAsDataURL(file);
     reader.onload = function(e){
         var pic = document.getElementById("preview");
         pic.src=this.result;
     }
 }


// 创建项目
    var create_project = function(){
        var pro_name = $('#inputProjectName').val(),
            pro_intro = $('#inputProjectIntro').val(),
            pro_part = $('#participant-project').val(),
            file = document.getElementById("f");
        console.log(file.files[0])
        var data = new FormData();
        data.append('pro_name',pro_name);
        data.append('pro_intro', pro_intro);
        data.append('pro_part', pro_part);
        data.append('pro_img', file.files[0])
        $.ajax({
            url: '/create_project/',
            type:'POST',
            dataType:'json',
            data: data,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(res){
                if (res.result){
                    $('#myModal').modal('hide');
                    layer.msg('项目创建成功', {icon: 6, time: 2000},function(){
                        window.location.href='/index'
                    });
                }else{
                     layer.msg(res.message, {icon: 5});
                }
            }
        })

    }
    $('#create-project-btn').click(create_project)
    //修改排版
    $('.typesetting li a').click(function(){
        $('.typesetting li a').removeClass('type-click')
        $(this).addClass('type-click')
        $('.typesetting li a span').removeClass('type-click')
        $(this).find('span').addClass('type-click')
        var typesetting = $(this).attr('id')
        setCookie('typesetting',typesetting,365)
        console.log("dsasdaas")
    })

    //设置排版cookie
    function getCookie(c_name)
    {
        if (document.cookie.length>0)
          {
          c_start=document.cookie.indexOf(c_name + "=")
          if (c_start!=-1)
            {
            c_start=c_start + c_name.length+1
            c_end=document.cookie.indexOf(";",c_start)
            if (c_end==-1) c_end=document.cookie.length
            return unescape(document.cookie.substring(c_start,c_end))
            }
          }
        return ""
    }

    function setCookie(c_name,value,expiredays)
    {
        var exdate=new Date()
        exdate.setDate(exdate.getDate()+expiredays)
        document.cookie=c_name+ "=" +escape(value)+
        ((expiredays==null) ? "" : ";expires="+exdate.toGMTString())
    }

    function checkCookie()
    {
        typesetting=getCookie('typesetting')
        if (typesetting!=null && typesetting!="")
          {
              if(typesetting == 'one'){
                  $('#one').click()
              }else{
                  $('#two').click()
              }
          }
        else
          {
          typesetting=1
          if (typesetting!=null && typesetting!="")
            {
            setCookie('typesetting',typesetting,365)
            }
          }
    }
    checkCookie();
})




// 用户首次登陆时，检测是否已经设置cookie
$(document).ready(function(){
  // 如果有cookie 且未失效，这里可以完善逻辑提高安全性
  if(getCookie('userId') != 'anonymous'){
    console.log(getCookie('userId'));
  }else{
    // 没有cookie信息，弹出modal用户进行授权
    $('#myModal').modal('show');
    // do something else, 可以用转圈来替代弹框，此次为了演示和用户感知
  }
})
// 绑定同意按钮
$('#auth_confirm').click(function(){ 
  userid = $('#modal_userinfo').text();
  if(userid != null){
    setCookie('userId', userid);
  }   
  else{
    console.log('获取用户信息失败！')    
  }
  location.reload();  
})
// modal内容加载事件绑定
$('#authModal').on('show.bs.modal', function(){
  // 执行一些动作...
  HWH5.getAuthCode({
    clientId: ''
  }).then(data => {
    console.log(data);
    _code = data.code;
    var _server = '/userid/';
    _url = _server + _code;       
    // make ajax req here to get user id
    $.ajax({
      url: _url,
      beforeSend: function(){
        $('#modal_userinfo').empty().append('<b>'+ '请稍等..' +'</b>');
        $('#auth_confirm').attr('disabled', true);  
      },
      success : function(result){
        $('#auth_confirm').attr('disabled', false);
        console.log('已进入获取用户信息接口');
        if(result.code === '0'){
          console.log(result.userId);
          $('#modal_userinfo').empty().append('<b>'+ result.userId +'</b>');
        }else{
          console.log(result.message);
          $('#modal_userinfo').empty().append('<b>'+ result.message +'</b>');
        }          
      }
    });
  }).catch(error => {
      console.log('获取异常', error);
  });
})
// 设置cookie
function setCookie(name, value){
  var Days = 30; 
  var exp = new Date(); 
  exp.setTime(exp.getTime() + Days*24*60*60*1000); 
  document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString() + ";path=/";
}
// 获取cookie
function getCookie(name) 
{ 
  var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)"); 
  if(arr=document.cookie.match(reg)) 
      return unescape(arr[2]); 
  else 
      return null; 
}
// 删除cookie
function delCookie(name){
  var exp = new Date(); 
  exp.setTime(exp.getTime() - 1); 
  var cval=getCookie(name); 
  if(cval!=null) 
      document.cookie= name + "=" + cval + ";expires=" + exp.toGMTString()+ ";path=/"; 
}
// 删除用户信息
function delUserId(){
  console.log('删除cookie信息！');
  delCookie('userId');
  location.reload();
  // 删除之前的绑定关系...
}

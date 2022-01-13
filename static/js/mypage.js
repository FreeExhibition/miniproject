function login() {
    window.location.href = '/login';
}

$(document).ready(function () {
    let token = document.cookie.split('=')[0];
    let localId = localStorage.getItem("userId");
    console.log(localId)
    if (token) {
        $('#loginBtn').text('로그아웃').attr("onclick", "logout()")
        $('#regBtn').hide();
    }
})

// 로그아웃은 내가 가지고 있는 토큰만 쿠키에서 없애면 됩니다.
function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃 되었습니다!')
    window.location.href = '/'
}

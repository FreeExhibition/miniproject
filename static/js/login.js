function login() {
    let userId = $("#userId").val()
    let userPwd = $("#userPwd").val()

    if (userId == "") {
        $("#helpIdLogin").text("아이디를 입력해주세요.")
        $("#userId").focus()
        return;
    } else {
        $("#helpIdLogin").text("")
    }

    if (userPwd == "") {
        $("#helpPwLogin").text("비밀번호를 입력해주세요.")
        $("#userPwd").focus()
        return;
    } else {
        $("#helpPwLogin").text("")
    }
    $.ajax({
        type: "POST",
        url: "/users/login",
        data: {
            userId_give: userId,
            userPw_give: userPwd
        },
        success: function (response) {
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                localStorage.setItem("userId", userId);
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}
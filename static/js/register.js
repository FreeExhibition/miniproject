function register() {
    let userId = $("#userId").val()
    let userPwd = $("#userPwd").val()
    let pwdCheck = $("#pwdCheck").val()
    console.log(userId, userPwd, pwdCheck)

    if ($("#helId").hasClass("is-danger")) {
        alert("아이디를 다시 확인해주세요.")
        return;
    } else if (!$("#helpId").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.")
        return;
    }

    if (userPwd == "") {
        $("#helpPw").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#userPwd").focus()
        return;
    } else if (!is_password(userPwd)) {
        $("#helpPw").text("비밀번호 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
        $("#userPwd").focus()
        return
    } else {
        $("#helpPw").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
    }
    if (pwdCheck == "") {
        $("#helpPwCheck").text("비밀번호를 다시 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#pwdCheck").focus()
        return;
    } else if (pwdCheck != userPwd) {
        $("#helpPwCheck").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
        $("#pwdCheck").focus()
        return;
    } else {
        $("#helpPwCheck").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
    }
    $.ajax({
        type: "POST",
        url: "/users/register",
        data: {
            userId_give: userId,
            userPw_give: userPwd
        },
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/login")
        }
    });

}

<!--  아이디 정규식  -->
function isUser(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[a-zA-Z0-9]{2,10}$/;
    return regExp.test(asValue);
}

<!--  비밀번호 정규식  -->
function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}

<!--  아이디 중복 체크  -->
function checkDup() {
    let userId = $("#userId").val()
    console.log(userId)
    if (userId == "") {
        $("#helpId").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
        $("#userId").focus()
        return;
    }
    if (!isUser(userId)) {
        $("#helpId").text("아이디 형식을 확인해주세요. 영문과 숫자만 사용 가능. 2-10자 길이").removeClass("is-safe").addClass("is-danger")
        $("#userId").focus()
        return;
    }
    $("#helpId").addClass("is-loading")
    $.ajax({
        type: "POST",
        url: "/users/checkDup",
        data: {
            userid_give: userId
        },
        success: function (response) {

            if (response["exists"]) {
                $("#helpId").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                $("#userId").focus()
            } else {
                $("#helpId").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
            }
            $("#helpId").removeClass("is-loading")

        }
    });
}
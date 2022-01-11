// 로그인 버튼 클릭 시 로그인 화면 이동
let token = document.cookie.split('=')[0]

function moveLoginPage() {
    window.location.href = '/login'
}

function addReview() {

    if (!token) {
        alert('로그인을 해주세요.')
        return
    }

    const contentVal = $('#inputContent').val();
    const exhibitionId = window.location.pathname.split('/')[2]
    if (!contentVal) {
        alert('리뷰를 작성해 주세요');
        return
    }

    $.ajax({
        type: "POST",
        url: "/reviews",
        data: {exhibitionId_give: exhibitionId, content_give: contentVal},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload()
        },
    })


}

// ajax review delete 요청
function deleteReview(id) {
    $.ajax({
        type: 'DELETE',
        url: `/reviews/${id}`,
        data: {id_give: id},
        success: function (response) {
            alert(response['msg']);
            window.location.reload()
        }
    });

}
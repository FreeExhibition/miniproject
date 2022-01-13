// 로그인 버튼 클릭 시 로그인 화면 이동
window.onload = () => {
    getReview();
    renderNav();
}

function login() {
    window.location.href = '/login';
}

function logout() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    const presentPath = location.pathname
    let validate = presentPath.split('/')[1];
    if (validate != ' ') {
        localStorage.setItem('backPath', presentPath);
    }

    window.location.reload();
}


function renderNav() {
    const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('mytoken='));

    if (token) {
        $('#loginBtn').text('로그아웃').attr("onclick", "logout()")
        $('#regBtn').text('마이페이지').attr("onclick", "window.location.href='/mypage'")
        return
    }
}

function getReview() {
    $('#reviewBox').empty();

    const id = window.location.pathname.split('/')[2]
    const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('mytoken='));
    const user = localStorage.getItem('userId')

    $.ajax({
        type: "GET",
        url: `/reviews/${id}`,
        data: {},
        success: function (response) {
            const allReviews = response['allReviews'];
            allReviews.map((review) => {
                let {user_id2: userId, content, exhibition_id2: reviewId} = review;
                if (token && userId === user) {
                    const temp_html = `<div class="review-box">
                        <div>
                            <strong class="user-id">${userId}</strong>
                            <p class="review-cotent">${content}</p>
                        </div>
                        <button class="delete" onclick="deleteReview(${reviewId})"></button>
                    </div>`
                    $('#reviewBox').append(temp_html);
                } else {
                    const temp_html = `<div class="review-box">
                        <div>
                        <strong class="user-id">${userId}</strong>
                        <p class="review-cotent">${content}</p>
                        </div>
                    </div>`
                    $('#reviewBox').append(temp_html);
                }
            })
        }
    })
}

function addReview() {
    let token = document.cookie.split('=')[0];
    if (!token) {
        alert('로그인을 해주세요.');
        return
    }
    ;

    const contentVal = $('#inputContent').val();
    const exhibitionId = window.location.pathname.split('/')[2]
    if (!contentVal) {
        alert('리뷰를 작성해 주세요');
        return
    }
    ;

    $.ajax({
        type: "POST",
        url: "/reviews",
        data: {exhibitionId_give: exhibitionId, content_give: contentVal},
        success: function (response) {
            alert(response["msg"]);
            getReview();
        },
    });
};

// ajax review delete 요청
function deleteReview(id) {

    $.ajax({
        type: 'DELETE',
        url: `/reviews/${id}`,
        data: {id_give: id},
        success: function (response) {
            alert(response['msg']);
            getReview();
        }
    });

}
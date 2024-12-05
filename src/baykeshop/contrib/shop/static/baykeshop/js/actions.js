const modalObject = {
    // 打开模态框
    openModal: function($el){
        $el.classList.add('bk-is-active');
    },
    // 关闭模态框
    closeModal: function($el){
        $el.classList.remove('bk-is-active');
    },
    // 关闭所有模态框
    closeAllModal: function($modals){
        // const $modals = document.querySelectorAll('.modal') || [];
        $modals.forEach($modal => {
            this.closeModal($modal);
        })
    },
    // 点击关闭事件
    clickCloseModal: function($modal_receipt){
        const $close_buttons = document.querySelectorAll('.bk-modal-background, .bk-modal-close, .cancel') || [];
        $close_buttons.forEach(item => {
            item.addEventListener('click', function () {
                modalObject.closeModal($modal_receipt);
            })
        })
    },

    // 点击确认事件
    clickConfirmModal: function($modal_receipt){
        const $confirm_button = document.querySelector('#modal-receipt-confirm')
        $confirm_button.addEventListener('click', async function () {
            let $receipt_api = $modal_receipt.getAttribute('data-api')
            fetch($receipt_api, {
                method: 'POST',
                credentials: "same-origin",
                headers: {
                    'X-CSRFToken': bayke.csrftoken
                }
            }).then(response => {
                console.log(response)
                return response.json()
            })
            .then(data => {
                if (data.code == 200) {
                    window.location.reload()
                } else {
                    bayke.message.error(data.msg)
                }
            })
        })
    }

}
// 确认收货
document.addEventListener('DOMContentLoaded', function () {
    const $receipt_buttons = document.querySelectorAll('.receipt') || [];
    const $modal_receipt = document.querySelector('#modal-receipt')
    // 关闭事件
    modalObject.clickCloseModal($modal_receipt);
    // 确认收货弹窗
    $receipt_buttons.forEach(item => {
        item.addEventListener('click', function () {
            let $receipt_api = item.getAttribute('data-api')
            $modal_receipt.setAttribute('data-api', $receipt_api)
            modalObject.openModal($modal_receipt)
       })
    })
    // 点击确认事件
    modalObject.clickConfirmModal($modal_receipt)
})

// 订单评价
document.addEventListener('DOMContentLoaded', function () {
    const $comment_buttons = document.querySelectorAll('.comment') || [];
    const $modal_comment = document.querySelector('#modal-comment')

    // 关闭事件
    modalObject.clickCloseModal($modal_comment);
    // 评价弹窗
    $comment_buttons.forEach(item => {
        item.addEventListener('click', function () {
            let $comment_api = item.getAttribute('data-api')
            let $form = $modal_comment.querySelector('form')
            $form.setAttribute('action', $comment_api)
            modalObject.openModal($modal_comment)
       })
    })
})
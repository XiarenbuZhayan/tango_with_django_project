// 购物车功能
function handleCart() {
    // 这里可以添加购物车相关功能
    console.log('购物车功能');
}

// 搜索功能
function handleSearch() {
    // 这里可以添加搜索相关功能
    console.log('搜索功能');
}

// 当DOM加载完成后绑定事件
document.addEventListener('DOMContentLoaded', function() {
    const cartBtn = document.querySelector('a[href="#"].btn-outline-dark:has(i.bi-cart)');
    const searchBtn = document.querySelector('a[href="#"].btn-outline-dark:has(i.bi-search)');
    
    if (cartBtn) {
        cartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            handleCart();
        });
    }
    
    if (searchBtn) {
        searchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            handleSearch();
        });
    }
}); 
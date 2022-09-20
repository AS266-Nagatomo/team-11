//アコーディオンをクリックした時の動作
$('.accordion_title').on('click', function() {//タイトル要素をクリックしたら
	$('.box').slideUp(500);//クラス名.boxがついたすべてのアコーディオンを閉じる

	var findElm = $(this).next(".box");//タイトル直後のアコーディオンを行うエリアを取得

	if($(this).hasClass('accordion_close')){//タイトル要素にクラス名closeがあれば
		$(this).removeClass('accordion_close');//クラス名を除去
	}else{//それ以外は
		$('.accordion_close').removeClass('accordion_close'); //クラス名closeを全て除去した後
		$(this).addClass('accordion_close');//クリックしたタイトルにクラス名closeを付与し
		$(findElm).slideDown(500);//アコーディオンを開く
	}
});

//ページが読み込まれた際にopenクラスをつけ、openがついていたら開く動作※不必要なら下記全て削除
$(window).on('load', function(){
	$('.accordion-area li:first-of-type section').addClass("accordion_open"); //accordion-areaのはじめのliにあるsectionにopenクラスを追加
	$(".accordion_open").each(function(index, element){	//openクラスを取得
		var Title =$(element).children('.accordion_title');	//openクラスの子要素のtitleクラスを取得
		$(Title).addClass('accordion_close');				///タイトルにクラス名closeを付与し
		var Box =$(element).children('.box');	//openクラスの子要素boxクラスを取得
		$(Box).slideDown(500);					//アコーディオンを開く
	});
});
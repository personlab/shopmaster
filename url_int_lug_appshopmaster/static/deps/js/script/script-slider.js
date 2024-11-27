// Responsive navigation menu
 const menuBtn = document.querySelector(".menu-btn");
 const navigationBtnsMenu = document.querySelector(".navigation");

 menuBtn.addEventListener("click", () => {
	menuBtn.classList.toggle("active");
	navigationBtnsMenu.classList.toggle("active");
 });






// Limit slider paragraph text characters and add "..." + read more button with a link.
document.addEventListener("DOMContentLoaded", function () {
	// Limit slider paragraph text
	const slideParagraphs = document.querySelectorAll(".slide-paragraph");

	slideParagraphs.forEach((slideParagraph) => {
		const textLimit = 100;
		const fullText = slideParagraph.innerText;
		const aTag = slideParagraph.querySelector(".paragraph-anchor-tag");

		if (slideParagraph.innerText.length > textLimit) {
			slideParagraph.innerHTML = fullText.substring(0, textLimit) + "... " + aTag.innerHTML;
		}
	});

	// Limit video card paragraph text
	const videoParagraphs = document.querySelectorAll(".video-paragraph");

	videoParagraphs.forEach((videoParagraph) => {
		const textLimit = 100;
		const fullText = videoParagraph.innerText;
		const aTag = videoParagraph.querySelector(".video-anchor-tag");


		if (videoParagraph.innerText.length > textLimit) {
			videoParagraph.innerHTML = fullText.substring(0, textLimit) + "... " + aTag.innerHTML;
		}
	});
});

// Load first slide
window.addEventListener("DOMContentLoaded", () => {
	const firstSlide = document.querySelector(".first-slide");
	const firstSlideBtn = document.querySelector(".first-slide-btn");
	const firstIndicatoBar = document.querySelector(".first-indicator-bar");

	setTimeout(() => {
		firstSlide.classList.add("active");
	}, 300);

	firstSlideBtn.classList.add("active");
	firstIndicatoBar.classList.add("active");
});

// Javascript for slider
const slider = document.querySelector(".slider");
const slides = slider.querySelectorAll(".slide");
const numberOfSlides = slides.length;
const slideBtns = document.querySelectorAll(".slide-btn");
const slideIndicatorBars = document.querySelectorAll(".indicator-bar");
var slideNumber = 0;

// Slider autoplay
var playSlider;

var repeater = () => {
	playSlider = setInterval(function () {
		slides.forEach((slide) => {
			slide.classList.remove("active");
		});

		slideBtns.forEach((slideBtn) => {
			slideBtn.classList.remove("active");
		});

		slideIndicatorBars.forEach((slideIndicatorBar) => {
			slideIndicatorBar.classList.remove("active");
		});

		slideNumber++;

		if (slideNumber > (numberOfSlides - 1)) {
			slideNumber = 0;
		}

		slides[slideNumber].classList.add("active");
		slideBtns[slideNumber].classList.add("active");
		slideIndicatorBars[slideNumber].classList.add("active");
	}, 8500);
}
repeater();

// Slider next/prev buttons navigation.
const nextBtn = document.querySelector(".next-btn");
const prevBtn = document.querySelector(".prev-btn");

// Slider next button navigation.
nextBtn.addEventListener("click", () => {
	slides.forEach((slide) => {
		slide.classList.remove("active");
	});

	slideBtns.forEach((slideBtn) => {
		slideBtn.classList.remove("active");
	});

	slideIndicatorBars.forEach((slideIndicatorBar) => {
		slideIndicatorBar.classList.remove("active");
	});

	slideNumber++;

	if (slideNumber > (numberOfSlides - 1)) {
		slideNumber = 0;
	}

	slides[slideNumber].classList.add("active");
	slideBtns[slideNumber].classList.add("active");
	slideIndicatorBars[slideNumber].classList.add("active");

	clearInterval(playSlider);
	repeater();
});

// Slider previous button navigation.
prevBtn.addEventListener("click", () => {
	slides.forEach((slide) => {
		slide.classList.remove("active");
	});

	slideBtns.forEach((slideBtn) => {
		slideBtn.classList.remove("active");
	});

	slideIndicatorBars.forEach((slideIndicatorBar) => {
		slideIndicatorBar.classList.remove("active");
	});

	slideNumber--;

	if (slideNumber < 0) {
		slideNumber = numberOfSlides - 1;
	}

	slides[slideNumber].classList.add("active");
	slideBtns[slideNumber].classList.add("active");
	slideIndicatorBars[slideNumber].classList.add("active");

	clearInterval(playSlider);
	repeater();
});

// Slider pagination.
var slideBtnNav = function (slideBtnClick) {
	slides.forEach((slide) => {
		slide.classList.remove("active");
	});

	slideBtns.forEach((slideBtn) => {
		slideBtn.classList.remove("active");
	});

	slideIndicatorBars.forEach((slideIndicatorBar) => {
		slideIndicatorBar.classList.remove("active");
	});

	slides[slideBtnClick].classList.add("active");
	slideBtns[slideBtnClick].classList.add("active");
	slideIndicatorBars[slideBtnClick].classList.add("active");
}

slideBtns.forEach((slideBtn, i) => {
	slideBtn.addEventListener("click", () => {
		slideBtnNav(i);
		clearInterval(playSlider);
		repeater();
		slideNumber = i;
	});
});

// Javascript for video modals.

slides.forEach((slide, i) => {
	let watchVideoBtn = slide.querySelector(".watch-video-btn");
	let slideVideoModal = slide.querySelector(".slide-video-modal");
	let videoModalContent = slide.querySelector(".video-modal-content");
	let videoCloseBtn = slide.querySelector(".video-close-btn");
	let animalVideo = slide.querySelector(".animal-video")

	// Open video modals on click watch video button.
	watchVideoBtn.addEventListener("click", () => {
		slideVideoModal.classList.add("active")

		setTimeout(() => {
			videoModalContent.classList.add("active");
		}, 300);
		
		// Play animal video on click watch video button.
		animalVideo.play();

		// stop slider autoplay on click watch video button
		if (slideVideoModal.classList.contains("active")) {
			clearInterval(playSlider);
		}

	});

	// // Reset current slide autoplay time on mouseover the slide video modal.
	// slideVideoModal.addEventListener("mouseover", () => {
	// 	// Restart the current slider indicator bar on click the video close button
	// 	clearInterval(playSlider);
	// });

	// Close video modals on click video modals close button.
	const videoClose = function(closeBtnClick) {
		slideIndicatorBars.forEach((slideIndicatorBar) => {
			slideIndicatorBar.classList.remove("active");
		});

		setTimeout(() => {
			slideIndicatorBars[closeBtnClick].classList.add("active");
		}, 0);
	}


	videoCloseBtn.addEventListener("click", () => {
		slideVideoModal.classList.remove("active");
		videoModalContent.classList.remove("active");

		slideIndicatorBars.forEach((slideIndicatorBar) => {
			slideIndicatorBar.classList.remove("active");
		});

		// Pause animal video on click video close button.
		animalVideo.pause();

		clearInterval(playSlider);
		repeater();
		videoClose(i);
	});
});

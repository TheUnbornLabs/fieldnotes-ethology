
(function(){
  // Quiz widgets: live progress + scored check
  var quizzes = document.querySelectorAll('.quiz-widget');
  quizzes.forEach(function(form){
    var answers = JSON.parse(form.dataset.answers || '{}');
    var questions = form.querySelectorAll('.quiz-question');
    var bar = form.querySelector('.quiz-progress-bar');
    var answeredEl = form.querySelector('.quiz-answered');

    function updateProgress(){
      var answered = form.querySelectorAll('input[type=radio]:checked').length;
      if(bar){ bar.style.width = Math.round((answered / questions.length) * 100) + '%'; }
      if(answeredEl){ answeredEl.textContent = answered; }
    }
    form.addEventListener('change', updateProgress);

    form.addEventListener('submit', function(e){
      e.preventDefault();
      var correct = 0;
      questions.forEach(function(q){
        var num = q.dataset.qnum;
        var checked = q.querySelector('input[type=radio]:checked');
        var feedback = q.querySelector('.quiz-feedback');
        var answer = answers[num];
        q.classList.remove('correct','incorrect');
        if(!checked){
          feedback.hidden = false;
          feedback.textContent = 'No answer selected. Correct answer: ' + answer;
          q.classList.add('incorrect');
          return;
        }
        var isCorrect = checked.value === answer;
        if(isCorrect){ correct++; q.classList.add('correct'); }
        else { q.classList.add('incorrect'); }
        feedback.hidden = false;
        feedback.textContent = isCorrect ? 'Correct!' : ('Incorrect. Correct answer: ' + answer);
      });
      var scoreEl = form.querySelector('.quiz-score');
      scoreEl.hidden = false;
      scoreEl.textContent = 'Score: ' + correct + ' / ' + questions.length;
      var first = form.querySelector('.quiz-question.incorrect, .quiz-question.correct');
      if(first){ first.scrollIntoView({behavior:'smooth', block:'center'}); }
    });
  });

  // Home / glossary search
  var searchInput = document.getElementById('site-search');
  if(searchInput){
    var base = searchInput.dataset.base || '';
    var results = document.getElementById('search-results');
    var catalog = null;
    fetch(base + 'catalog.json').then(function(r){ return r.json(); }).then(function(data){ catalog = data; });

    function render(items){
      if(!items.length){
        results.innerHTML = '<div class="sr-empty">No matches.</div>';
        results.hidden = false;
        return;
      }
      results.innerHTML = items.slice(0,12).map(function(r){
        var href = base + r.category + 's/' + r.slug + '/index.html';
        return '<a href="' + href + '">' + String(r.number).padStart(3,'0') + ' — ' + r.commonName + ' (' + r.scientificName + ')</a>';
      }).join('');
      results.hidden = false;
    }

    searchInput.addEventListener('input', function(){
      var q = searchInput.value.trim().toLowerCase();
      if(!q || !catalog){ results.hidden = true; return; }
      var items = catalog.filter(function(r){
        return (r.commonName + ' ' + r.scientificName + ' ' + r.hook + ' ' + r.summaryText).toLowerCase().indexOf(q) !== -1;
      });
      render(items);
    });
    document.addEventListener('click', function(e){
      if(!results.contains(e.target) && e.target !== searchInput){ results.hidden = true; }
    });
  }

  // Glossary filter
  var glossaryFilter = document.getElementById('glossary-filter');
  if(glossaryFilter){
    var entries = document.querySelectorAll('#glossary-content .gloss-entry');
    var sections = document.querySelectorAll('#glossary-content section');
    var alphaNav = document.querySelector('.alpha-nav');
    var emptyMsg = document.getElementById('glossary-empty');
    glossaryFilter.addEventListener('input', function(){
      var q = glossaryFilter.value.trim().toLowerCase();
      var anyVisible = false;
      sections.forEach(function(sec){
        var sectionHasMatch = false;
        sec.querySelectorAll('.gloss-entry').forEach(function(entry){
          var text = entry.textContent.toLowerCase();
          var match = !q || text.indexOf(q) !== -1;
          entry.hidden = !match;
          if(match){ sectionHasMatch = true; anyVisible = true; }
        });
        sec.hidden = !sectionHasMatch;
      });
      if(alphaNav){ alphaNav.hidden = q.length > 0; }
      if(emptyMsg){ emptyMsg.hidden = anyVisible; }
    });
  }

  // Active section highlighting in the species-page table of contents
  var toc = document.querySelector('.toc');
  if(toc){
    var tocLinks = toc.querySelectorAll('a[href^="#"]');
    var linkFor = {};
    tocLinks.forEach(function(a){ linkFor[a.getAttribute('href').slice(1)] = a; });
    var sections = document.querySelectorAll('.book-body section[id]');
    if('IntersectionObserver' in window && sections.length){
      var current = null;
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            if(current) current.classList.remove('active');
            current = linkFor[entry.target.id];
            if(current) current.classList.add('active');
          }
        });
      }, {rootMargin: '-15% 0px -70% 0px', threshold: 0});
      sections.forEach(function(s){ observer.observe(s); });
    }
  }

  // Back-to-top button
  var backToTop = document.getElementById('back-to-top');
  if(backToTop){
    window.addEventListener('scroll', function(){
      backToTop.classList.toggle('visible', window.scrollY > 600);
      backToTop.hidden = false;
    }, {passive:true});
    backToTop.addEventListener('click', function(){
      window.scrollTo({top:0, behavior:'smooth'});
    });
  }
})();


(function(){
  var quizzes = document.querySelectorAll('.quiz-widget');
  quizzes.forEach(function(form){
    var answers = JSON.parse(form.dataset.answers || '{}');
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var questions = form.querySelectorAll('.quiz-question');
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
    });
  });

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
})();

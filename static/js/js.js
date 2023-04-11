function gera_cor(qtd=1){
    var bg_color = []
    var border_color = []
    for(let i = 0; i < qtd; i++){
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }

    return [bg_color, border_color];

}

function renderiza_cumprimento(url){
  fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

      const ctx = document.getElementById('cumprimento_curriculo').getContext('2d');
      var cores_cumprimento = gera_cor(2);
      const myChart = new Chart(ctx, {
        type: 'pie',
        data:{
          labels:['Cumprimento', 'Não cumprimento'],
          datasets: [{
            label: 'Cumprimento',
            data:[data.totalV, data.totalF],
            backgroundColor: cores_cumprimento[0],
            border_color: cores_cumprimento[9],
            borderWidth: 1
          }],
        },
      });

    });
}

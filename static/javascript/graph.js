let title = document.getElementById("chart_title").value;
let target = document.getElementById("chart_target").value;
let dstr = String(document.getElementById("chart_data").value);
let darr = dstr.split(",");
let dlabel = String(document.getElementById("chart_labels").value);
let larr = dlabel.split(",");
let ctx = document.getElementById("myChart").getContext("2d");
let myRadarChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: larr,
    datasets: [
      {
        label: "系列A",
        data: darr,
        backgroundColor: "rgba(255,0,0,0.2)",
        borderColor: "red",
        borderWidth: 2,
        pointStyle: "circle",
        pointRedius: 6,
        pointBorderColor: "red",
        pointBorderWidth: 2,
        pointBackgroundColor: "yellow",
        pointLablelFontSize: 20,
      },
    ],
  },
  options: {
    responsive: false,
    title: {
      display: true,
      fontSize: 20,
      text: title,
    },
    legend: {
      position: "bottom",
      labels: {
        fontSize: 20,
      },
    },
    gridLines: {
      display: true,
      color: "lime",
    },
  },
});

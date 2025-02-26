 let chart = new Chart( "#chart", { // or DOM element
    data: {
      labels: ["Exam 1", "Exam 2", "Exam 3", "Exam 4",
      "Exam 5", "Exam 6", "Exam 7", "Exam 8"],

      datasets: [
        {
          label: "Some Data", type: 'bar',
          values: [25, 40, 30, 35, 8, 52, 17, -4]
        },
        {
          label: "Another Set", type: 'bar',
          values: [25, 50, -10, 15, 18, 32, 27, 14]
        },
        {
          label: "Yet Another", type: 'line',
          values: [15, 20, -3, -15, 58, 12, -17, 37]
        }
      ],

      yMarkers: [{ label: "Marker", value: 70 }],
      yRegions: [{ label: "Region", start: -10, end: 50 }]
    },

    title: "Performace",
    type: 'bar', // or 'bar', 'line', 'pie', 'percentage'
    height: 250,
    colors: ['purple', '#ffa3ef', 'red']
});


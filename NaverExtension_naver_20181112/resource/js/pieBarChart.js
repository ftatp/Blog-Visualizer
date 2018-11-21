console.log("check pieBar");
var g_radius = 0;
var width = 230;
var height = 277;
// var radius = Math.min(width, height) / 2;
var radius = 65;
console.log("Radius: ", radius)

function drawPie(names, datas) {
    var pie_data = datas;
    var pie_name = names;
    var radar_render = d3.select("#total_left").append("svg"),
        //width = svg.attr("width"),
        //height = svg.attr("height"),
        //radius = Math.min(width, height) / 2,
        g = radar_render.append("g")
            .attr("transform", "translate(" + width / 2.0 + "," + height / 2.0 + ")");

    var color = d3.scaleOrdinal(['#4daf4a','#377eb8','#ff7f00']);

    // Generate the pie
    var pie = d3.pie();

    // Generate the arcs
    var arc = d3.arc()
        .innerRadius(30)
        .outerRadius(radius-5);

    // Generate the arc
    var label = d3.arc()
        .outerRadius(radius)
        .innerRadius(radius - 80);

    // Generate groups
    var arcs = g.selectAll("arc")
        .data(pie(pie_data))
        .enter()
        .append("g")
        .attr("class", "arc")

    // Draw arc paths
    arcs.append("path")
        .attr("fill", function(d, i) {
            return color(i);
        })
        .attr("d", arc);

    // Pie text 넣는 곳
    arcs.append("text")
        .attr("transform", function(d, i) {
            if (i == 0) { // 글의 구조
                return "translate(" + label.centroid(d) + ")";
            }
            else if (i == 1){ // 기타
                return "translate(" + (label.centroid(d)[0] - 18) + "," + (label.centroid(d)[1] + 27) + ")";
            }
            
            else { // 글의 감정
                return "translate(" + (label.centroid(d)[0] - 33) + "," + (label.centroid(d)[1] - 5) + ")";
            }
        })
        .text(function(d, i) { return pie_name[i]; });

    // 원 둘레로 막대 그래프 그리기
    var circle_center_x = width / 2;
    var circle_center_y = height / 2;

    var data = [0.1, 0.3, 0.7, 0.2, 1.2, 0.5, 0.7, 0.8, 1.7, 1.2,
                0.1, 0.3, 0.7, 0.2, 1.2, 0.5, 0.7, 0.8, 1.7, 1.2,
                0.1, 0.3, 0.7, 0.2, 1.2, 0.5, 0.7, 0.8, 1.7, 1.2];

    // draw bar chart
    // 우선 하나의 바가 차지할 수 있는 넓이를 구하기
    var circumference = radius * 2 * Math.PI;
    var bar_area_width = (circumference / data.length) - 5; // height
    // bar chart 그리기
    for (var i = 0; i < data.length; i++) {
        // 이번 차례에 그릴 바의 '크기' 구하기
        var rect_size = data[i] * 4;
        // 이번 차례에 그릴 바의 '각도' 구하기
        var theta = (2 * Math.PI) * (i / data.length); // 0 ~ 2 * PI
        var degree = theta * (180 / Math.PI);
        // 이번 차례에 그릴 바의 위치 구하기
        var bar_x = circle_center_x + (Math.cos(theta) * radius);
        var bar_y = circle_center_y + (Math.sin(theta) * radius);

        // bar chart 색깔 별로 칠하기
        // 인덱스의 시작은 글의 구조 부터
        (function () {
            // 글의 구조 범위 0 ~ 4 / 23 ~ 31
            if (i >= 23 || i < 5) {
                radar_render.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_size * 7)
                    .attr('height', bar_area_width)
                    .attr('transform', 'translate(' + bar_x + ',' + bar_y + ') rotate(' + (degree + 5) + ')')
                    .attr('fill', '#4daf4a')
                    .attr('opacity', 0.5)
                    .attr('stroke', '#555');
            }
            // 기타 범위 5 ~ 17
            if (i > 4 && i < 18) {
                radar_render.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_size * 7)
                    .attr('height', bar_area_width)
                    .attr('transform', 'translate(' + bar_x + ',' + bar_y + ') rotate(' + (degree + 5) + ')')
                    .attr('fill', '#377eb8')
                    .attr('opacity', 0.5)
                    .attr('stroke', '#555');
            }
            // 글의 감정 범위 18 ~ 22
            if (i >= 18 && i < 23) {
                radar_render.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_size * 7)
                    .attr('height', bar_area_width)
                    .attr('transform', 'translate(' + bar_x + ',' + bar_y + ') rotate(' + (degree + 5) + ')')
                    .attr('fill', '#ff7f00')
                    .attr('opacity', 0.5)
                    .attr('stroke', '#555');
            }
        }) ();
    }
}
function drawPie2(names, datas) {
    var pie_data = datas;
    var pie_name = names;
    var radar_render = d3.select("#total_right").append("svg"),
        //width = svg.attr("width"),
        //height = svg.attr("height"),
        //radius = Math.min(width, height) / 2,
        g = radar_render.append("g")
            .attr("transform", "translate(" + width / 2.0 + "," + height / 2.0 + ")");

    var color = d3.scaleOrdinal(['#4daf4a','#377eb8','#ff7f00']);

    // Generate the pie
    var pie = d3.pie();

    // Generate the arcs
    var arc = d3.arc()
        .innerRadius(30)
        .outerRadius(radius-5);

    // Generate the arc
    var label = d3.arc()
        .outerRadius(radius)
        .innerRadius(radius - 80);

    // Generate groups
    var arcs = g.selectAll("arc")
        .data(pie(pie_data))
        .enter()
        .append("g")
        .attr("class", "arc")

    // Draw arc paths
    arcs.append("path")
        .attr("fill", function(d, i) {
            return color(i);
        })
        .attr("d", arc);

    // Pie text 넣는 곳
    arcs.append("text")
        .attr("transform", function(d, i) {
            if (i == 0) { // 글의 구조
                return "translate(" + label.centroid(d) + ")";
            }
            else if (i == 1){ // 기타
                return "translate(" + (label.centroid(d)[0] - 18) + "," + (label.centroid(d)[1] + 27) + ")";
            }

            else { // 글의 감정
                return "translate(" + (label.centroid(d)[0] - 33) + "," + (label.centroid(d)[1] - 5) + ")";
            }
        })
        .text(function(d, i) { return pie_name[i]; });

    // 원 둘레로 막대 그래프 그리기
    var circle_center_x = width / 2;
    var circle_center_y = height / 2;

    var data = [0.5, 0.3, 0.7, 0.2, 1.2, 0.8, 0.7, 0.8, 0.8, 1.4,
        0.1, 0.3, 1.0, 0.4, 1.0, 0.3, 0.7, 0.9, 1.1, 1.2,
        0.1, 0.3, 0.7, 0.2, 1.2, 0.5, 0.7, 0.8, 1.2, 1.5];

    // draw bar chart
    // 우선 하나의 바가 차지할 수 있는 넓이를 구하기
    var circumference = radius * 2 * Math.PI;
    var bar_area_width = (circumference / data.length) - 5; // height
    // bar chart 그리기
    for (var i = 0; i < data.length; i++) {
        // 이번 차례에 그릴 바의 '크기' 구하기
        var rect_size = data[i] * 4;
        // 이번 차례에 그릴 바의 '각도' 구하기
        var theta = (2 * Math.PI) * (i / data.length); // 0 ~ 2 * PI
        var degree = theta * (180 / Math.PI);
        // 이번 차례에 그릴 바의 위치 구하기
        var bar_x = circle_center_x + (Math.cos(theta) * radius);
        var bar_y = circle_center_y + (Math.sin(theta) * radius);

        // bar chart 색깔 별로 칠하기
        // 인덱스의 시작은 글의 구조 부터
        (function () {
            // 글의 구조 범위 0 ~ 4 / 23 ~ 31
            if (i >= 23 || i < 5) {
                radar_render.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_size * 7)
                    .attr('height', bar_area_width)
                    .attr('transform', 'translate(' + bar_x + ',' + bar_y + ') rotate(' + (degree + 5) + ')')
                    .attr('fill', '#4daf4a')
                    .attr('opacity', 0.5)
                    .attr('stroke', '#555');
            }
            // 기타 범위 5 ~ 17
            if (i > 4 && i < 18) {
                radar_render.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_size * 7)
                    .attr('height', bar_area_width)
                    .attr('transform', 'translate(' + bar_x + ',' + bar_y + ') rotate(' + (degree + 5) + ')')
                    .attr('fill', '#377eb8')
                    .attr('opacity', 0.5)
                    .attr('stroke', '#555');
            }
            // 글의 감정 범위 18 ~ 22
            if (i >= 18 && i < 23) {
                radar_render.append('rect')
                    .attr('x', 0)
                    .attr('y', 0)
                    .attr('width', rect_size * 7)
                    .attr('height', bar_area_width)
                    .attr('transform', 'translate(' + bar_x + ',' + bar_y + ') rotate(' + (degree + 5) + ')')
                    .attr('fill', '#ff7f00')
                    .attr('opacity', 0.5)
                    .attr('stroke', '#555');
            }
        }) ();
    }
}
var feature_set_names = ['글의 구조', '기타 정보', '글의 감정'];
var feature_nums = [13, 13, 5];
var structure_features = ['img img img img img', 'img img img img text', 'img img img text img', 'img img text img img', 'img img text img text', 'img text img img img', 'img text img img text', 'img text img text img', 'text img img img img', 'text img img img text', 'text img img text img', 'text img text img img', 'text img text img text'];
var sentiment_features = ['pos_ratio', 'neg_ratio', 'subjectivity', 'polarity', 'senti_diffs_per_ref'];
var others_features = ['Question_count', 'First_ratio', 'Second_ratio', 'Tag_count', 'Sticker_count', 'Text_len', 'Count_space_mistake', 'effort_ratio', 'effort_img_ratio', 'Left', 'Center', 'Right', 'Justify'];

drawPie(feature_set_names, feature_nums);
drawPie2(feature_set_names, feature_nums);

d3.csv("../resource/data/cluster_mean.csv", function(error, data) {
    if (error) {
        console.log("error!!!")
    }
    drawPie(feature_set_names, feature_nums);
    drawPie2(feature_set_names, feature_nums);

    //console.log("0: ", data[0]);
    //console.log("5: ", data[5]);

    // var current_structure_values = [];
    // var cluster5_structure_values = [];
    //
    // for (var i = 0; i < structure_features.length; i++){
    //     current_structure_values.push(cluster0[structure_features[i]]);
    //     cluster5_structure_values.push(cluster5[structure_features[i]]);
    // }
    //
    // console.log("a: ", current_structure_values);
    // console.log("b: ", cluster5_structure_values);
});




// // Generate the arcs
// var arc = d3.arc()
//             .innerRadius(0)
//             .outerRadius(radius);
// console.log("arc: ", arc);
//
// // Generate groups
// var arcs = g.selectAll("arc")
//     .data(pie(data))
//     .enter()
//     .append("g")
//     .attr("class", "arc");
//
// arcs.append("text")
//     .attr("transform", function(data) {
//         return "translate(" + label.centroid(data) + ")";
//     })
//     .text(function(data) {return data; });
//
// // Draw arc paths
// arcs.append("path")
//     .attr("fill", function(d, i){
//         return color(i);
//     })
//     .attr("d", arc);
// // arc에 대한 시작 각도와 끝 각도를 계산
// var pie = d3.pie()
// console.log(pie(data))

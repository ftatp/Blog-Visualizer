console.log("check RadarScript");
var w = 175,
    h = 185;

var colorscale = ['#eaec96', '#43c0ac', '#a93199', '#fa0559', '#6b76ff',
                  '#6b76ff', '#ff7657', '#74b49b', '#ffcd3c', '#7acfdf'];

//Legend titles
var LegendOptions = ['Credible','Non-Credible'];
var structure_features = ['img img img img img', 'img img img img text', 'img img img text img', 'img img text img img', 'img img text img text',
                           'img text img img img', 'img text img img text', 'img text img text img', 'text img img img img', 'text img img img text',
                            'text img img text img', 'text img text img img', 'text img text img text'];
var view_structure_features = ['iiiii', 'iiiiT', 'iiiTi', 'iiTii', 'iiTiT', 'iTiii', 'iTiiT', 'iTiTi', 'Tiiii', 'TiiiT', 'TiiTi', 'TiTii', 'TiTiT'];

var sentiment_features = ['pos_ratio', 'neg_ratio', 'subjectivity', 'polarity', 'senti_diffs_per_ref'];
var view_sentiment_features = ['긍정 비율', '부정 비율', '주관성', '극성', '감정 점수']

var others_features = ['Question_count', 'First_ratio', 'Second_ratio', 'Tag_count', 'Sticker_count', 'Text_len', 'Count_space_mistake', 'effort_ratio', 'effort_img_ratio', 'Left', 'Center', 'Right', 'Justify'];
var view_others_features = ['물음표', '1인칭', '2인칭', '태그', '스티커', '글의 길이', '문법 실수', '글 비율', '이미지 비율', '좌측 정렬', '중앙 정렬', '우측 정렬', '양쪽 정렬'];
var temp_data0 = [0.096026642, 0.007879821, -0.046426936, 0.265603797, 0.11470556, -0.031447504, 0.052394985, -0.131920436,
                   0.116591163,	0.384132386, -0.006651071, 0.010915931, 0.017798507, 0.131733408, -0.026036593, 0.031615233, 0.001390753,
                   -0.018321461, -0.32131619, -0.262142211, -0.161207726, -0.076996365, 1.475743411, -0.191489533, 1.228736,
                    0.489271439, -0.273179417, -0.077114481, 1.184616708, 1.432105524, 0.063919546];

var temp_data5 = [0.056026642, 0.067879821, -0.166426936, 0.265603797, 0.11470556, -0.131447504, 0.022394985, -0.101920436,
                    0.076591163,	0.154132386, -0.506651071, 0.080915931, 0.317798507, 0.131733408, -0.036036593, 0.051615233, 0.007390753,
                    -0.038321461, -0.22131619, -0.162142211, -0.181207726, -0.036996365, 1.275743411, -0.191489533, 1.228736,
                    0.349271439, -0.383179417, -0.077114481, 1.184616708, 1.232105524, 0.083919546];

// 임시용
function temp_return_cluster_value(data, features){   // data, features
    var cluster_data = [];
    for (var i = 0; i < features.length; i ++){
        cluster_data.push(data[i]);
    }
    return cluster_data;
}

// // cluster_value 구하기, csv용
// function return_cluster_value(data, features){   // data, features
//     var cluster_data = [];
//     for (var i = 0; i < features.length; i ++){
//         cluster_data.push(data[features[i]]);
//     }
//     console.log("cluster_data: ", cluster_data);
//     return cluster_data;
// }

// data type 맞추기
function change_data_type(data, features){
    var cluster_data = []; // 최종 형태
    var cluster_list = [];
    for (var i = 0; i < features.length; i ++){
        var cluster_dict = {};
        for (var j = 0; j < features.length; j ++){
            cluster_dict['axis'] = features[i];
            cluster_dict['value'] = data[i];
        }
        cluster_list.push(cluster_dict);
    }
    cluster_data.push(cluster_list);
    return cluster_data;
}

//Data
var path = '../resource/data/cluster_mean.csv';
d3.csv(path, function(error, data) {
    if (error) {
        console.log("error!!!")
    }
    // structure
    var cluster0_structure_value = temp_return_cluster_value(temp_data0, structure_features);
    var cluster0_structure_data = change_data_type(cluster0_structure_value, view_structure_features);
    var cluster5_structure_value = temp_return_cluster_value(temp_data5, structure_features);
    var cluster5_structure_data = change_data_type(cluster5_structure_value, view_structure_features);
    // sentiment
    var cluster0_sentiment_value = temp_return_cluster_value(temp_data0, sentiment_features);
    var cluster0_sentiment_data = change_data_type(cluster0_sentiment_value, view_sentiment_features);
    var cluster5_sentiment_value = temp_return_cluster_value(temp_data5, sentiment_features);
    var cluster5_sentiment_data = change_data_type(cluster5_sentiment_value, view_sentiment_features);
    // others
    var cluster0_others_value = temp_return_cluster_value(temp_data0, others_features);
    var cluster0_ohters_data = change_data_type(cluster0_others_value, view_others_features);
    var cluster5_others_value = temp_return_cluster_value(temp_data5, others_features);
    var cluster5_others_data = change_data_type(cluster5_others_value, view_others_features);

    //Options for the Radar chart, other than default
    var mycfg = {
        w: w,
        h: h,
        maxValue: 0.6,
        levels: 6,
        ExtraWidthX: 300
    }

    //Call function to draw the Radar chart
    //Will expect that data is in %'s
    RadarChart3.draw("#structure_left", cluster0_structure_data, mycfg);
    RadarChart4.draw("#structure_right", cluster5_structure_data, mycfg);

    RadarChart3.draw("#sentiment_left", cluster0_sentiment_data, mycfg);
    RadarChart4.draw("#sentiment_right", cluster5_sentiment_data, mycfg);

    RadarChart.draw("#others_left", cluster0_ohters_data, mycfg);
    RadarChart2.draw("#others_right", cluster5_others_data, mycfg);

    // call the plot function
    // RadViz()
    //     .DOMTable(IDtable)
    //     .DOMRadViz(IDradviz)
    //     .TableTitle(titles)
    //     .ColorAccessor(colorAccessor)
    //     .Dimensionality(dimensions)
    //     .DAnchor(dimensionAnchor)
    //     .DATA(data)
    //     .call();
});

// temp
// 대명사 사용 빈도 ( 'First_ratio', 'Second_ratio')
// 글의 스타일 ( 'Question_count', 'Tag_count', 'Sticker_count')
// 글의 정성 ( 'Text_len',  'effort_ratio', 'effort_img_ratio', 'Count_space_mistake',)
// 글의 정렬 ( 'Left', 'Center', 'Right', 'Justify')

// // 원본 데이터
// var d = [
//     [
//         {axis:"Email", value:0.59},
//         {axis:"Social Networks",value:0.56},
//         {axis:"Internet Banking",value:0.42},
//         {axis:"News Sportsites",value:0.34},
//         {axis:"Search Engine",value:0.48},
//         {axis:"View Shopping sites",value:0.14},
//         {axis:"Paying Online",value:0.11},
//         {axis:"Buy Online",value:0.05},
//         {axis:"Stream Music",value:0.07},
//         {axis:"Online Gaming",value:0.12},
//         {axis:"Navigation",value:0.27},
//         {axis:"App connected to TV program",value:0.03},
//         {axis:"Offline Gaming",value:0.12},
//     ]
// ];



////////////////////////////////////////////
/////////// Initiate legend ////////////////
////////////////////////////////////////////

// function () {
//
// }
// var svg = d3.select('#body')
//     .selectAll('svg')
//     .append('svg')
//     .attr("width", w+300)
//     .attr("height", h)

// //Create the title for the legend
// var text = svg.append("text")
//     .attr("class", "title")
//     .attr('transform', 'translate(90,0)')
//     .attr("x", w - 30)
//     .attr("y", 10)
//     .attr("font-size", "12px")
//     .attr("fill", "#404040")
//     .text("What % of owners use a specific service in a week");
//
// //Initiate Legend
// var legend = svg.append("g")
//     .attr("class", "legend")
//     .attr("height", 100)
//     .attr("width", 240)
//     .attr('transform', 'translate(140,20)');

// //Create colour squares
// legend.selectAll('rect')
//     .data(LegendOptions)
//     .enter()
//     .append("rect")
//     .attr("x", w - 65)
//     .attr("y", function(d, i){ return i * 20;})
//     .attr("width", 10)
//     .attr("height", 10)
//     .style("fill", function(d, i){ return colorscale(i);});

// //Create text next to squares
// legend.selectAll('text')
//     .data(LegendOptions)
//     .enter()
//     .append("text")
//     .attr("x", w - 52)
//     .attr("y", function(d, i){ return i * 20 + 9;})
//     .attr("font-size", "11px")
//     .attr("fill", "#737373")
//     .text(function(d) { return d; });

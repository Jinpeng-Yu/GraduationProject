$(function () {
  echarts_1();
  echarts_2();
  echarts_4();
  // echarts_31();
  // echarts_32();
  // echarts_33();
  echarts_5();
  // echarts_6();

  function echarts_1() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echart1'));

    const data = {
      in: [
        ['2021-03-30 00:00:00', 123],
        ['2021-03-30 00:00:01', 55],
        ['2021-03-30 00:00:02', 23],
        ['2021-03-30 00:00:03', 123],
        ['2021-03-30 00:00:04', 552],
        ['2021-03-30 00:00:05', 22],
      ],
    }

    $.ajax({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/data_visual',
      data: {video_name : window.sessionStorage.getItem('video_name')},
      error: function () {
        // alert('获取折线图数据失败!')
        // this.$message('获取折线图数据失败!')
      },
      success: function (res) {
        // this.$message.success('获取折线图数据成功')
        // alert('获取折线图数据成功')
        data['in'] = res.data
        // console.log(data['in'])

        option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#dddc6b'
              }
            }
          },
          legend: {
            top:'0%',
            data:['保有量'],
            textStyle: {
              color: 'rgba(255,255,255,.5)',
              fontSize:'12',
            }
          },
          grid: {
            left: '10',
            top: '30',
            right: '10',
            bottom: '10',
            containLabel: true
          },

          xAxis: [{
            type: 'time',   // x轴为 时间轴
            splitLine: { show: false },
            boundaryGap: false,
            axisLabel:  {
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize:12,
              },
            },
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.2)',
                width: 0
              }
            },
            axisTick: { show: false },
            data: data['in'].map(function (item) {
              return item[0]
            })
          }, {
            axisPointer: {show: false},
            axisLine: {  show: false},
            position: 'bottom',
            offset: 20,
          }],

          yAxis: [{
            type: 'value',
            axisTick: {show: false},
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            },
            axisLabel:  {
              // formatter: '{value} 人',
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize:12,
              },
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            }
          }],
          series: [
            {
              name: '保有量',
              type: 'line',
              smooth: true,
              symbol: 'circle',
              symbolSize: 5,
              showSymbol: false,
              lineStyle: {
                normal: {
                  color: '#0184d5',
                  width: 2
                }
              },
              areaStyle: {
                normal: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(1, 132, 213, 0.4)'
                  }, {
                    offset: 0.8,
                    color: 'rgba(1, 132, 213, 0.1)'
                  }], false),
                  shadowColor: 'rgba(0, 0, 0, 0.1)',
                }
              },
              itemStyle: {
                normal: {
                  color: '#0184d5',
                  borderColor: 'rgba(221, 220, 107, .1)',
                  borderWidth: 12
                }
              },
              connectNulls: true,
              data: data['in']
            },

          ]

        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
          myChart.resize();
        });

      }
    })
  }
  function echarts_2() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echart2'));

    const data = {
      valid: 0,
      invalid: 0,
    }

    $.ajax({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/manager_status_visual',
      // data: {video_name : window.sessionStorage.getItem('video_name')},
      error: function () {
        // alert('获取数据失败!')
        // this.$message('获取数据失败!')
      },
      success: function (res) {
        // this.$message.success('获取数据成功')
        // alert('获取数据成功')
        data['valid'] = res.valid
        data['invalid'] = res.invalid

        option = {
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)",
            position:function(p){   //其中p为当前鼠标的位置
              return [p[0] + 10, p[1] - 10];
            }
          },
          legend: {
            top:'85%',
            itemWidth: 10,
            itemHeight: 10,
            data:['有效管理权限','无效管理权限'],
            textStyle: {
              color: 'rgba(255,255,255,.5)',
              fontSize:'12',
            }
          },
          series: [
            {
              name:'权限分布',
              type:'pie',
              center: ['50%', '42%'],
              radius: ['30%', '70%'],
              color: ['#065aab','#06f0ab'],
              label: {show:false},
              labelLine: {show:false},
              data:[
                {value:data['valid'], name:'有效管理权限'},
                {value:data['invalid'], name:'无效管理权限'},
              ]
            }
          ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
          myChart.resize();
        });
      }
    })
  }
  function echarts_4() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echart4'));

    const data = {
      in: [
        ['2021-03-30 00:00:00', 123],
        ['2021-03-30 00:00:01', 55],
        ['2021-03-30 00:00:02', 23],
        ['2021-03-30 00:00:03', 123],
        ['2021-03-30 00:00:04', 552],
        ['2021-03-30 00:00:05', 22],
      ],
    }

    $.ajax({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/data_visual',
      data: {video_name : window.sessionStorage.getItem('video_name')},
      error: function () {
        // alert('获取折线图数据失败!')
        // this.$message('获取折线图数据失败!')
      },
      success: function (res) {
        // this.$message.success('获取折线图数据成功')
        // alert('获取折线图数据成功')
        data['in'] = res.data
        // console.log(data['in'])

        option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              lineStyle: {
                color: '#dddc6b'
              }
            }
          },
          legend: {
            top:'0%',
            data:['保有量'],
            textStyle: {
              color: 'rgba(255,255,255,.5)',
              fontSize:'12',
            }
          },
          grid: {
            left: '10',
            top: '30',
            right: '10',
            bottom: '10',
            containLabel: true
          },

          xAxis: [{
            type: 'time',   // x轴为 时间轴
            splitLine: { show: false },
            boundaryGap: false,
            axisLabel:  {
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize:12,
              },
            },
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.2)',
                width: 0
              }
            },
            axisTick: { show: false },
            data: data['in'].map(function (item) {
              return item[0]
            })
          }, {
            axisPointer: {show: false},
            axisLine: {  show: false},
            position: 'bottom',
            offset: 20,
          }],

          yAxis: [{
            type: 'value',
            axisTick: {show: false},
            axisLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            },
            axisLabel:  {
              // formatter: '{value} 人',
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize:12,
              },
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(255,255,255,.1)'
              }
            }
          }],
          visualMap: {
            // top: 50,
            // right: 0,
            show:false,
            pieces: [{
              gt: 0,
              lte: 5,
              color: '#93CE07'
            }, {
              gt: 5,
              lte: 10,
              color: '#FBDB0F'
            }, {
              gt: 10,
              lte: 20,
              color: '#FC7D02'
            }, {
              gt: 20,
              lte: 30,
              color: '#FD0100'
            }, {
              gt: 30,
              lte: 40,
              color: '#AA069F'
            }, {
              gt: 40,
              color: '#AC3B2A'
            }],
            outOfRange: {
              color: '#999'
            }
          },
          series: [
            {
              name: '保有量',
              type: 'line',
              smooth: true,
              symbol: 'circle',
              symbolSize: 5,
              showSymbol: false,
              // lineStyle: {
              //   normal: {
              //     color: '#0184d5',
              //     width: 2
              //   }
              // },
              // areaStyle: {
              //   normal: {
              //     color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
              //       offset: 0,
              //       color: 'rgba(1, 132, 213, 0.4)'
              //     }, {
              //       offset: 0.8,
              //       color: 'rgba(1, 132, 213, 0.1)'
              //     }], false),
              //     shadowColor: 'rgba(0, 0, 0, 0.1)',
              //   }
              // },
              // itemStyle: {
              //   normal: {
              //     color: '#0184d5',
              //     borderColor: 'rgba(221, 220, 107, .1)',
              //     borderWidth: 12
              //   }
              // },
              // markLine: {
              //   silent: true,
              //   lineStyle: {
              //     color: '#333'
              //   },
              //   data: [{
              //     yAxis: 5
              //   }, {
              //     yAxis: 10
              //   }, {
              //     yAxis: 20
              //   }, {
              //     yAxis: 30
              //   }, {
              //     yAxis: 40
              //   }]
              // },
              connectNulls: true,
              data: data['in']
            },

          ]

        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
          myChart.resize();
        });

      }
    })
  }
  function echarts_5() {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('echart5'));

    const data = {
      regionValue: [],
    }

    $.ajax({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/data_region_visual',
      data: {video_name: window.sessionStorage.getItem('video_name')},
      error: function () {
        // alert('获取数据失败!')
      },
      success: function (res) {
        // alert('获取数据成功')
        data['regionValue'] = res.regionValue
        // console.log(data['regionValue'])

        option = {
          //  backgroundColor: '#00265f',
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow'}
          },
          grid: {
            left: '0%',
            top:'10px',
            right: '0%',
            bottom: '4%',
            containLabel: true
          },
          xAxis: [{
            type: 'category',
            data: ['0-5', '5-10', '10-20', '20-30', '30-40', '40+'],
            axisLine: {
              show: true,
              lineStyle: {
                color: "rgba(255,255,255,.1)",
                width: 1,
                type: "solid"
              },
            },

            axisTick: {
              show: false,
            },
            axisLabel:  {
              interval: 0,
              // rotate:50,
              show: true,
              splitNumber: 15,
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: '12',
              },
            },
          }],
          yAxis: [{
            type: 'value',
            axisLabel: {
              formatter: '{value} s',
              show:true,
              textStyle: {
                color: "rgba(255,255,255,.6)",
                fontSize: '12',
              },
            },
            axisTick: {
              show: false,
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: "rgba(255,255,255,.1	)",
                width: 1,
                type: "solid"
              },
            },
            splitLine: {
              lineStyle: {
                color: "rgba(255,255,255,.1)",
              }
            }
          }],
          series: [
            {

              type: 'bar',
              data: data['regionValue'],
              barWidth:'35%', //柱子宽度
              // barGap: 1, //柱子之间间距
              itemStyle: {
                normal: {
                  color:'#27d08a',
                  color: function (params) {
                    var colorList = [
                      '#93CE07',
                      '#FBDB0F',
                      '#FC7D02',
                      '#FD0100',
                      '#AA069F',
                      '#AC3B2A',
                      '#999',
                    ];
                    return colorList[params.dataIndex]
                  },
                  opacity: 1,
                  barBorderRadius: 5,
                }
              }
            }

          ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        window.addEventListener("resize",function(){
          myChart.resize();
        });

      }
    })
  }

  // function echarts_6() {
  //   // 基于准备好的dom，初始化echarts实例
  //   var myChart = echarts.init(document.getElementById('echart6'));
  //
  //   var dataStyle = {
  //     normal: {
  //       label: {
  //         show: false
  //       },
  //       labelLine: {
  //         show: false
  //       },
  //       //shadowBlur: 40,
  //       //shadowColor: 'rgba(40, 40, 40, 1)',
  //     }
  //   };
  //   var placeHolderStyle = {
  //     normal: {
  //       color: 'rgba(255,255,255,.05)',
  //       label: {show: false,},
  //       labelLine: {show: false}
  //     },
  //     emphasis: {
  //       color: 'rgba(0,0,0,0)'
  //     }
  //   };
  //   option = {
  //     color: ['#0f63d6', '#0f78d6', '#0f8cd6', '#0fa0d6', '#0fb4d6'],
  //     tooltip: {
  //       show: true,
  //       formatter: "{a} : {c} "
  //     },
  //     legend: {
  //       itemWidth: 10,
  //       itemHeight: 10,
  //       itemGap: 12,
  //       bottom: '3%',
  //
  //       data: ['浙江', '上海', '广东', '北京', '深圳'],
  //       textStyle: {
  //         color: 'rgba(255,255,255,.6)',
  //       }
  //     },
  //
  //     series: [
  //       {
  //         name: '浙江',
  //         type: 'pie',
  //         clockWise: false,
  //         center: ['50%', '42%'],
  //         radius: ['59%', '70%'],
  //         itemStyle: dataStyle,
  //         hoverAnimation: false,
  //         data: [{
  //           value: 80,
  //           name: '01'
  //         }, {
  //           value: 20,
  //           name: 'invisible',
  //           tooltip: {show: false},
  //           itemStyle: placeHolderStyle
  //         }]
  //       },
  //       {
  //         name: '上海',
  //         type: 'pie',
  //         clockWise: false,
  //         center: ['50%', '42%'],
  //         radius: ['49%', '60%'],
  //         itemStyle: dataStyle,
  //         hoverAnimation: false,
  //         data: [{
  //           value: 70,
  //           name: '02'
  //         }, {
  //           value: 30,
  //           name: 'invisible',
  //           tooltip: {show: false},
  //           itemStyle: placeHolderStyle
  //         }]
  //       },
  //       {
  //         name: '广东',
  //         type: 'pie',
  //         clockWise: false,
  //         hoverAnimation: false,
  //         center: ['50%', '42%'],
  //         radius: ['39%', '50%'],
  //         itemStyle: dataStyle,
  //         data: [{
  //           value: 65,
  //           name: '03'
  //         }, {
  //           value: 35,
  //           name: 'invisible',
  //           tooltip: {show: false},
  //           itemStyle: placeHolderStyle
  //         }]
  //       },
  //       {
  //         name: '北京',
  //         type: 'pie',
  //         clockWise: false,
  //         hoverAnimation: false,
  //         center: ['50%', '42%'],
  //         radius: ['29%', '40%'],
  //         itemStyle: dataStyle,
  //         data: [{
  //           value: 60,
  //           name: '04'
  //         }, {
  //           value: 40,
  //           name: 'invisible',
  //           tooltip: {show: false},
  //           itemStyle: placeHolderStyle
  //         }]
  //       },
  //       {
  //         name: '深圳',
  //         type: 'pie',
  //         clockWise: false,
  //         hoverAnimation: false,
  //         center: ['50%', '42%'],
  //         radius: ['20%', '30%'],
  //         itemStyle: dataStyle,
  //         data: [{
  //           value: 50,
  //           name: '05'
  //         }, {
  //           value: 50,
  //           name: 'invisible',
  //           tooltip: {show: false},
  //           itemStyle: placeHolderStyle
  //         }]
  //       }, ]
  //   };
  //
  //   // 使用刚指定的配置项和数据显示图表。
  //   myChart.setOption(option);
  //   window.addEventListener("resize",function(){
  //     myChart.resize();
  //   });
  // }
  // function echarts_31() {
  //   // 基于准备好的dom，初始化echarts实例
  //   var myChart = echarts.init(document.getElementById('fb1'));
  //   option = {
  //
  //     title: [{
  //       text: '年龄分布',
  //       left: 'center',
  //       textStyle: {
  //         color: '#fff',
  //         fontSize:'16'
  //       }
  //
  //     }],
  //     tooltip: {
  //       trigger: 'item',
  //       formatter: "{a} <br/>{b}: {c} ({d}%)",
  //       position:function(p){   //其中p为当前鼠标的位置
  //         return [p[0] + 10, p[1] - 10];
  //       }
  //     },
  //     legend: {
  //
  //       top:'70%',
  //       itemWidth: 10,
  //       itemHeight: 10,
  //       data:['0岁以下','20-29岁','30-39岁','40-49岁','50岁以上'],
  //       textStyle: {
  //         color: 'rgba(255,255,255,.5)',
  //         fontSize:'12',
  //       }
  //     },
  //     series: [
  //       {
  //         name:'年龄分布',
  //         type:'pie',
  //         center: ['50%', '42%'],
  //         radius: ['40%', '60%'],
  //         color: ['#065aab', '#066eab', '#0682ab', '#0696ab', '#06a0ab','#06b4ab','#06c8ab','#06dcab','#06f0ab'],
  //         label: {show:false},
  //         labelLine: {show:false},
  //         data:[
  //           {value:1, name:'0岁以下'},
  //           {value:4, name:'20-29岁'},
  //           {value:2, name:'30-39岁'},
  //           {value:2, name:'40-49岁'},
  //           {value:1, name:'50岁以上'},
  //         ]
  //       }
  //     ]
  //   };
  //
  //   // 使用刚指定的配置项和数据显示图表。
  //   myChart.setOption(option);
  //   window.addEventListener("resize",function(){
  //     myChart.resize();
  //   });
  // }
  // function echarts_32() {
  //   // 基于准备好的dom，初始化echarts实例
  //   var myChart = echarts.init(document.getElementById('fb2'));
  //   option = {
  //
  //     title: [{
  //       text: '职业分布',
  //       left: 'center',
  //       textStyle: {
  //         color: '#fff',
  //         fontSize:'16'
  //       }
  //
  //     }],
  //     tooltip: {
  //       trigger: 'item',
  //       formatter: "{a} <br/>{b}: {c} ({d}%)",
  //       position:function(p){   //其中p为当前鼠标的位置
  //         return [p[0] + 10, p[1] - 10];
  //       }
  //     },
  //     legend: {
  //
  //       top:'70%',
  //       itemWidth: 10,
  //       itemHeight: 10,
  //       data:['电子商务','教育','IT/互联网','金融','学生','其他'],
  //       textStyle: {
  //         color: 'rgba(255,255,255,.5)',
  //         fontSize:'12',
  //       }
  //     },
  //     series: [
  //       {
  //         name:'年龄分布',
  //         type:'pie',
  //         center: ['50%', '42%'],
  //         radius: ['40%', '60%'],
  //         color: ['#065aab', '#066eab', '#0682ab', '#0696ab', '#06a0ab','#06b4ab','#06c8ab','#06dcab','#06f0ab'],
  //         label: {show:false},
  //         labelLine: {show:false},
  //         data:[
  //           {value:5, name:'电子商务'},
  //           {value:1, name:'教育'},
  //           {value:6, name:'IT/互联网'},
  //           {value:2, name:'金融'},
  //           {value:1, name:'学生'},
  //           {value:1, name:'其他'},
  //         ]
  //       }
  //     ]
  //   };
  //
  //   // 使用刚指定的配置项和数据显示图表。
  //   myChart.setOption(option);
  //   window.addEventListener("resize",function(){
  //     myChart.resize();
  //   });
  // }
  // function echarts_33() {
  //   // 基于准备好的dom，初始化echarts实例
  //   var myChart = echarts.init(document.getElementById('fb3'));
  //   option = {
  //     title: [{
  //       text: '兴趣分布',
  //       left: 'center',
  //       textStyle: {
  //         color: '#fff',
  //         fontSize:'16'
  //       }
  //
  //     }],
  //     tooltip: {
  //       trigger: 'item',
  //       formatter: "{a} <br/>{b}: {c} ({d}%)",
  //       position:function(p){   //其中p为当前鼠标的位置
  //         return [p[0] + 10, p[1] - 10];
  //       }
  //     },
  //     legend: {
  //       top:'70%',
  //       itemWidth: 10,
  //       itemHeight: 10,
  //       data:['汽车','旅游','财经','教育','软件','其他'],
  //       textStyle: {
  //         color: 'rgba(255,255,255,.5)',
  //         fontSize:'12',
  //       }
  //     },
  //     series: [
  //       {
  //         name:'兴趣分布',
  //         type:'pie',
  //         center: ['50%', '42%'],
  //         radius: ['40%', '60%'],
  //         color: ['#065aab', '#066eab', '#0682ab', '#0696ab', '#06a0ab','#06b4ab','#06c8ab','#06dcab','#06f0ab'],
  //         label: {show:false},
  //         labelLine: {show:false},
  //         data:[
  //           {value:2, name:'汽车'},
  //           {value:3, name:'旅游'},
  //           {value:1, name:'财经'},
  //           {value:4, name:'教育'},
  //           {value:8, name:'软件'},
  //           {value:1, name:'其他'},
  //         ]
  //       }
  //     ]
  //   };
  //
  //   // 使用刚指定的配置项和数据显示图表。
  //   myChart.setOption(option);
  //   window.addEventListener("resize",function(){
  //     myChart.resize();
  //   });
  // }
})

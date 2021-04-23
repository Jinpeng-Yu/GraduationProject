<template>
    <div>
      <!-- 面包屑导航区 -->
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>数据展示</el-breadcrumb-item>
        <el-breadcrumb-item>数据统计</el-breadcrumb-item>
      </el-breadcrumb>
      <!-- 卡片视图 -->
      <el-card>
        <!-- 2.为Echarts准备一个Dom -->
        <div id="main" style="width: 1000px;height:550px;margin-left:10%"></div>
      </el-card>
    </div>
</template>

<script>
    import echarts from "echarts";
    import {doubleChart} from "./Trends";
    const data = {
      in:[
        ['2021-03-30 00:00:00' , 123],
        ['2021-03-30 00:00:01' , 55],
        ['2021-03-30 00:00:02' , 23],
        ['2021-03-30 00:00:03' , 123],
        ['2021-03-30 00:00:04' , 552],
        ['2021-03-30 00:00:05' , 22],
      ],
    }
    export default {
        name: "Report",
      async mounted() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        const { data: res } = await this.$http.get('data_visual', {params:{video_name : window.sessionStorage.getItem('video_name')}})
        if (res.error_num !== 0) return this.$message('获取折线图数据失败!')
        else{
          this.$message.success('获取折线图数据成功')
          data['in'] = res.data
          // console.log(data['in'])
        }

        myChart.setOption(singleChart(data, 'crowd'))
      }
    }
    export const singleChart = (data, text) => {
      const type = text.split('$')[0]
      const unit = type === 'crowd' ? '人' : '人'
      const titles = type === 'crowd' ? ['入口保有量', '保有量'] : ['上行速率', '下行速率']
      return {
        title: {
          text: '人流量统计',
          left: '5%'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          backgroundColor: '#fff',
          padding: 10,
          textStyle: {
            fontSize: 12,
            color: '#152934',
            lineHeight: 24
          },
          extraCssText: 'box-shadow: 0 0 3px rgba(0, 0, 0, 0.3); border-radius: 0;',
          formatter: (params) => {
            var result = `${params[0].data[0]} <br/>`
            params.map(item => {
              result += `${item.seriesName} : ${isNaN(item.value[1]) ? '-' : item.value[1]} ${unit}</br>`
            })
            return result
          }
        },
        grid: {
          left: '5%',
          right: '15%',
          bottom: '10%',
          top: '15%'
        },
        yAxis: [
          {
            splitLine: {
              show: true,
              lineStyle: {
                type: 'dotted',
                color: 'rgba(155, 155, 155, 0.5)'
              }
            },
            axisLine: {
              show: false
            },
            axisLabel: {
              color: '#5A6872',
              fontSize: 11
            },
            axisTick: {show: false},
            type: 'value',
          }
        ],
        xAxis: [{
          type: 'time',   // x轴为 时间轴
          splitLine: {show: false},
          axisLine: {
            lineStyle: {width: 0}
          },
          axisLabel: {
            color: '#5A6872',
            fontSize: 11
          },
          axisTick: {show: false},
          boundaryGap: false,
          data: data['in'].map(function (item) {
            return item[0]
          })
        }],
        legend: {data: titles},
        // color: ['#41D6C3', '#5AAAFA'],
        visualMap: {
          top: 50,
          right: 0,
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
            name: type === 'crowd' ? '保有量' : '下行速率',
            type: 'line',
            symbol: 'none',
            markPoint: {
              label: {
                normal: {
                  show: true,
                  backgroundColor: '#fff',
                  position: 'top',
                  color: '#AC3B2A',
                  borderColor: 'rgba(90,170,250,0.3)',
                  borderWidth: 1,
                  padding: 8,
                  formatter: `{b}: {c} ${unit}`
                }
              },
              symbol: 'circle',
              itemStyle: {
                normal: {
                  borderColor: 'rgba(90,170,250,0.3)',
                  borderWidth: 15
                }
              },
              symbolSize: 7,
              data: [
                {type: 'max', name: 'Max'}
              ]
            },
            markLine: {
              silent: true,
              lineStyle: {
                color: '#333'
              },
              data: [{
                yAxis: 5
              }, {
                yAxis: 10
              }, {
                yAxis: 20
              }, {
                yAxis: 30
              }, {
                yAxis: 40
              }]
            },
            // lineStyle: {normal: {color: '#5AAAFA', width: 1}},
            // areaStyle: {normal: {color: '#5AAAFA', opacity: 0.5}},
            connectNulls: true,
            data: data['in']
          }
        ]
      }
    }
</script>

<style scoped>

</style>

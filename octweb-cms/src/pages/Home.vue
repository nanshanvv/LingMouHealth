<template>
  <div id="home"></div>
    <h1>首页</h1>
    <div class="oct-chart" id="board-post-count"></div>
    <div class="oct-chart" id="day7-post-count"></div>
</template>

<script>
import * as echarts from 'echarts';
import { ElMessage } from 'element-plus';
export default {
    name: "HomeItem",
    mounted(){
      this.loadBoardPostCountChart();
      this.load7DayPostCountChart();

    },
    methods:{
      loadBoardPostCountChart(){
          this.$http.getBoardPostCount().then(res =>{
            if(res['code']!=200){
              ElMessage.error(res['message'])
              return
            }
            var data = res['data']
            var board_names = data['board_names']
            var post_counts = data['post_counts']
            var chartDom = document.getElementById('board-post-count');
            var myChart = echarts.init(chartDom);
            var option;
            option = {
              title: {
                text: '板块帖子数量',
                x:'center',
                y:'bottom'
              },

              tooltip: {
              trigger: 'axis'
              },
              xAxis: {
                type: 'category',
                data: board_names
              },
              yAxis: {
                type: 'value'
              },
              series: [
                {
                  data: post_counts,
                  type: 'bar'
                }
              ]
        };
        option && myChart.setOption(option);
          }
            ) 

      },
      load7DayPostCountChart(){
        this.$http.getDay7PostCount().then(res =>{
        if(res['code']!=200){
          ElMessage.error(res['message'])
          return
        }
        var data = res['data']['dates']
        var counts =res['data']['counts']
        var chartDom = document.getElementById('day7-post-count');
        var myChart = echarts.init(chartDom);
        var option;

        option = {
          title: {
                text: '7日流量数据',
                x:'center',
                y:'bottom'
              },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              data: counts,
              type: 'line',
              areaStyle: {}
            }
          ]
        };

        option && myChart.setOption(option);
        })

      }
    }

}
</script>

<style scoped>
.oct-chart{
  height: 300px;
  width: 100%;
}

</style>
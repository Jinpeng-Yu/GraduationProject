<template>
  <div>
    <!-- 面包屑导航区 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>数据分析</el-breadcrumb-item>
      <el-breadcrumb-item>视频分析</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图 -->
    <el-card>
      <!-- 提示 -->
      <el-alert title="视频数据分析" type="info" center show-icon :closable="false"></el-alert>
      <!-- 步骤条 -->
      <el-steps :space="200" :active="activeIndex - 0" finish-status="success" simple style="margin-top: 20px">
        <el-step title="上传视频" icon="el-icon-upload"></el-step>
        <el-step title="视频分析" icon="el-icon-data-analysis"></el-step>
        <el-step title="分析结果" icon="el-icon-document"></el-step>
        <el-step title="完成" icon="el-icon-success"></el-step>
      </el-steps>

      <!-- Tab栏 -->
      <el-form
        :rules="addFormRules"
        label-width="100px"
        label-position="top"
      >
        <el-tabs
          v-model="activeIndex"
          :tab-position="'left'"
          :before-leave="beforeTabLeave"
          @tab-click="tabClicked"
        >
          <el-tab-pane label="上传视频" name="0">
            <el-form-item label="视频上传" prop="upload_video" enctype="multipart/form-data">
              <el-upload
                class="upload-demo"
                drag
                :disabled = "upload_success"
                :action = "uploadUrl"
                :show-file-list="false"
                :on-success="handleVideoSuccess"
                :before-upload="beforeUploadVideo"
                :on-progress="uploadVideoProcess"
                multiple>
                <video-player v-if="videoForm.Video !='' && videoFlag == false && upload_success == true"
                              class="video-player vjs-custom-skin"
                              :playsinline="true"
                              :options="playerOptions"
                controls="controls">您的浏览器不支持视频播放</video-player>
<!--                <i v-else-if="videoForm.Video =='' && videoFlag == false" class="el-icon-plus avatar-uploader-icon"></i>-->
                <el-progress v-if="videoFlag == true" type="circle" :percentage="videoUploadPercent" style="margin-top:30px;"></el-progress>
                <i v-else-if="videoForm.Video =='' && videoFlag == false" class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <div class="el-upload__tip" slot="tip">支持上传 mp4/avi 视频文件格式，且不超过300MB</div>
              </el-upload>
              <el-button type="primary" :disabled="!upload_success" @click="changeClick">更改</el-button>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="视频分析" name="1">
            <el-form-item
              v-loading="loading"
              element-loading-text="视频分析中"
              element-loading-spinner="el-icon-loading">
              <el-button  type="primary" @click="analyseClick" :disabled="analyse_success">开始分析</el-button>
            </el-form-item>
          </el-tab-pane>
          <el-tab-pane label="分析结果" name="2">
            <el-form-item>
              <div class="block">
                <video-player v-if="this.resultForm.Video != '' && analyse_success == true && upload_success == true"
                              class="video-player vjs-custom-skin"
                              :playsinline="true"
                              :options="resultOptions"
                              controls="controls">您的浏览器不支持视频播放</video-player>
              </div>
              <el-button size="small" type="success" class="displaybtn" icon="el-icon-s-opportunity" @click="displayClick">数据展示</el-button>
            </el-form-item>
          </el-tab-pane>
        </el-tabs>
      </el-form>
    </el-card>
  </div>
</template>

<script>
    export default {
        name: "Video",
      data (){
          return {
            // 步骤条默认激活 与左侧Tab联动
            activeIndex: '0',

            uploadUrl:"http://127.0.0.1:8000/api/upload_video",//你要上传视频到你后台的地址
            videoUploadPercent: "", //进度条的进度，
            videoFlag: false, //是否显示进度条
            videoForm: {
              Video: '',
              video_name: '',
            },
            resultForm: {
              Video: '',
            },

            // 视频上传成功
            upload_success: false,
            // 视频分析成功
            analyse_success: false,
            // 分析加载
            loading: false,

            // 视频播放
            playerOptions : {
              playbackRates : [ 0.5, 1.0, 1.5, 2.0 ], //可选择的播放速度
              autoplay : false, //如果true,浏览器准备好时开始回放。
              muted : false, // 默认情况下将会消除任何音频。
              loop : false, // 视频一结束就重新开始。
              preload : 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
              language : 'zh-CN',
              aspectRatio : '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
              fluid : true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
              sources : [ {
                type : "video/mp4",
                // src : require('../../assets/test.mp4')//url地址
                src : require('../../assets/ProcessedData/videos/demo.mp4')
              } ],
              poster : "", //你的封面地址
              // width: document.documentElement.clientWidth,
              // height: document.documentElement.clientHeight,
              notSupportedMessage : '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
              controlBar : {
                timeDivider : true,//当前时间和持续时间的分隔符
                durationDisplay : true,//显示持续时间
                remainingTimeDisplay : false,//是否显示剩余时间功能
                fullscreenToggle : true  //全屏按钮
              },
            },
            // 分析结果展示
            resultOptions : {
              playbackRates : [ 0.5, 1.0, 1.5, 2.0 ], //可选择的播放速度
              autoplay : false, //如果true,浏览器准备好时开始回放。
              muted : false, // 默认情况下将会消除任何音频。
              loop : false, // 视频一结束就重新开始。
              preload : 'auto', // 建议浏览器在<video>加载元素后是否应该开始下载视频数据。auto浏览器选择最佳行为,立即开始加载视频（如果浏览器支持）
              language : 'zh-CN',
              aspectRatio : '16:9', // 将播放器置于流畅模式，并在计算播放器的动态大小时使用该值。值应该代表一个比例 - 用冒号分隔的两个数字（例如"16:9"或"4:3"）
              fluid : true, // 当true时，Video.js player将拥有流体大小。换句话说，它将按比例缩放以适应其容器。
              sources : [ {
                type : "video/mp4",
                // src : require('../../assets/test.mp4')//url地址
                src : require('../../assets/ProcessedData/results/new_video2.mp4')
              } ],
              poster : "", //你的封面地址
              // width: document.documentElement.clientWidth,
              // height: document.documentElement.clientHeight,
              notSupportedMessage : '此视频暂无法播放，请稍后再试', //允许覆盖Video.js无法播放媒体源时显示的默认信息。
              controlBar : {
                timeDivider : true,//当前时间和持续时间的分隔符
                durationDisplay : true,//显示持续时间
                remainingTimeDisplay : false,//是否显示剩余时间功能
                fullscreenToggle : true  //全屏按钮
              },
            },
            addFormRules: {
              upload_video: [
                { required: true, message: '请上传视频', trigger: 'blur' }
              ]
            },
          }
      },
      methods: {
        // Tab标签被选中时触发
        tabClicked () {},
        // 上传前校验
        beforeUploadVideo(file) {
          const isLt300M = file.size / 1024 / 1024  < 300;
          if (['video/mp4','video/avi'].indexOf(file.type) == -1) {
            this.$message.error('请上传正确的视频格式');
            return false;
          }
          if (!isLt300M) {
            this.$message.error('上传视频大小不能超过300MB哦!');
            return false;
          }
        },
        // 上传进度显示
        uploadVideoProcess(event, file, fileList) {
          this.videoFlag = true;
          // this.videoUploadPercent = file.percentage.toFixed(0);
          this.videoUploadPercent = Math.floor(event.percent)
        },
        // 上传成功
        handleVideoSuccess(res, file) {                               //获取上传图片地址
          this.videoFlag = false;
          this.videoUploadPercent = 0;
          if(res.code == 200){
            this.$message.success('视频上传成功')
            // this.videoForm.videoUploadId = res.data.uploadId;
            this.videoForm.Video = '../../assets' + res.video_url;
            this.videoForm.video_name = res.video_name;
            // console.log(this.videoForm.Video)
            // this.playerOptions.sources.src = '../../assets' + res.video_url
            // console.log(this.playerOptions.sources.src)
            clearTimeout(this.timer)
            this.timer = setTimeout(()=>{
              this.playerOptions.sources[0].src = require('../../assets' + res.video_url)
              console.log(this.playerOptions.sources[0].src)
              this.upload_success = true
            }, 3000)
          }else{
            this.upload_success = false
            this.$message.error('视频上传失败，请重新上传！');
          }
        },
        beforeTabLeave(activeName, odlActiveName) {
          // 未选中商品分类阻止Tab标签跳转
          console.log(this.upload_success)
          if (odlActiveName === '0' && !this.upload_success) {
            this.$message.error('请先上传视频数据')
            return false
          }
          else if (odlActiveName === '1' && !this.analyse_success) {
            this.$message.error('请先分析视频数据')
            return false
          }
        },
        changeClick(){
          this.$message.info('请重新上传视频')
          this.videoUploadPercent= "" //进度条的进度，
          this.videoFlag= false //是否显示进度条
          this.videoForm.Video= ''
          this.upload_success = false
          this.loading = false
          this.resultForm.Video = ''
          this.analyse_success = false
        },
        async analyseClick(){
          this.loading = true
          this.$message.info('视频分析中，请耐心等待')
          clearTimeout(this.timer)
          const { data: res } = await this.$http.get('analyse_video', {params:{ video_name : this.videoForm.video_name}})
          this.timer = setTimeout(()=>{
            if (res.error_num !== 0) {
              this.$message.info('视频分析失败')
              this.analyse_success = false
            } else {
              this.resultForm.Video = res.result
              this.resultOptions.sources[0].src = require('../../assets/ProcessedData/results/' + res.result)
              this.$message.success('视频数据分析完成')
              this.loading = false
              this.analyse_success = true
              console.log(this.analyse_success)
            }
          }, 6000)
        },
        displayClick(){
          window.sessionStorage.setItem('activePath', '/trends')
          window.sessionStorage.setItem('video_name', this.videoForm.video_name)
          this.$router.push('/trends')
          // this.$router.go(0)
        },
      },
      activated() {
        this.displayClick()
      }
    }
</script>

<style scoped lang="less">
  .el-checkbox {
    margin: 0 8px 0 0 !important;
  }
  .previewImg{
    width: 100%;
  }
  .btnAdd{
    margin-top: 15px
  }
  .video-player {
    /*width: 178px;*/
    /*height: 178px;*/
    /*display: block;*/
    margin-left: 5%;
    width: 90%;
    height: 100%;
    object-fit: fill;
  }
  /*.video-avatar {*/
  /*  width: 400px;*/
  /*  height: 200px;*/
  /*}*/
  .block {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    /*overflow: hidden;*/
    width: 780px;
    height: 410px;
    margin-left: 13%;
  }
  .displaybtn {
    margin-left: 85%;
  }
</style>

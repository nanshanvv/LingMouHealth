<template>
    <div id="banner">
      <el-space direction="vertical" :size="20" style="width: 100%">
        <h1>轮播图管理</h1>
        <div style="text-align: right">
          <el-button type="primary" @click="onAddButtonClick">
            <el-icon><plus /></el-icon>
            添加轮播图
          </el-button>
        </div>
        <el-table :data="banners" style="width: 100%">
                <el-table-column prop="name" label="名称" width="180px" />
                <el-table-column prop="image_url" label="图片">
                    <template #default="scope">
                        <img :src="formatImageUrl(scope.row.image_url)" style="width: 200px; height: 100px;" />
                    </template>
                </el-table-column>
                <el-table-column prop="link_url" label="链接"  >
                    <template #default="scope">
                        <a :href="scope.row.link_url" target="_blank">{{ scope.row.link_url }}</a>
                    </template>
                </el-table-column>
                <el-table-column prop="priority" label="优先级" width="100px" />
                <el-table-column>
                    <template #default="scope">
                        <el-button type="primary" circle @click="onEditEvent(scope.$index)">
                        <el-icon><edit/></el-icon>
                        </el-button>
                        <el-button type="danger" :icon="Delete" circle @click="onDeleteEvent(scope.$index)">
                        <el-icon><delete/></el-icon>
                        </el-button>
                    </template>
                </el-table-column>

        </el-table>
      </el-space>

      <el-dialog v-model="bannerDialogVisible" title="添加轮播图" width="30%">
            <el-form :model="form" :rules="rules" ref="dialogForm">
            <el-form-item label="名字" prop="name">
                <el-input v-model="form.name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="图片" prop="image_url">
                <div style="display:flex">
                    <el-input v-model="form.image_url" autocomplete="off" style="margin-right: 10px;" />
                    <el-upload
                    :action="$http.server_host+'/cmsapi/banner/image/upload'"
                    name="image"
                    :headers="{'Authorization':'Bearer '+$auth.token}"
                    :show-file-list="false"
                    accept="image/jpg, image/png"
                    :on-success="onImageUploadSuccess"
                    :on-error="onImageUploadError"
                    >
                        <el-button type="primary">点击上传</el-button>

                    </el-upload>
                </div>
            </el-form-item>
            <el-form-item label="超链接" prop="link_url">
                <el-input v-model="form.link_url" autocomplete="off" />
            </el-form-item>
            <el-form-item label="优先级" prop="priority">
                <el-input v-model="form.priority" autocomplete="off" type="number" />
            </el-form-item>
            
            </el-form>
            <template #footer>
            <div class="dialog-footer">
                <el-button @click="bannerDialogVisible = false">Cancel</el-button>
                <el-button type="primary" @click="onDialogSubmitEvent">
                Confirm
                </el-button>
            </div>
            </template>
        </el-dialog>

            <!-- 删除轮播图确认对话框 -->
        <el-dialog
        v-model="deleteDialogVisible"
        title="提示"
        width="30%"
        >
        <span>您确定要删除这个轮播图吗？</span>
        <template #footer>
            <span class="dialog-footer">
            <el-button @click="deleteDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="onConfirmDeleteEvent">确定</el-button>
            </span>
        </template>
        </el-dialog>
    </div>
  </template>
  
  <script>
  import { Plus, Edit, Delete } from "@element-plus/icons";
  import { ElMessage } from 'element-plus'
  export default {
    name: "BannerItem",
    components: {
      Plus,
      Edit, 
      Delete
    },
    data(){
        return{
            bannerDialogVisible: false,
            deleteDialogVisible:false,
            deleteingIndex:0,
            editingIndex:0,
            banners:[],
            form: {
                name: "",
                image_url: "",
                link_url: "",
                priority: 0
            },
            rules: {
                name: [{required: true,message: '请输入轮播图名称！',trigger: 'blur'}],
                image_url: [{required: true, message: '必须上传轮播图~', trigger: 'blur'}],
                link_url: [{required: true, message: '必须输入轮播图跳转链接~', trigger: 'blur'}],
                priority: [
                    {required: true, message: '必须输入优先级~', trigger: 'blur'}
                ]

            }
        }
    },
    mounted() {
        this.$http.getBannerList().then(result => {
            let banners = result['data'];
            this.banners = banners;
        })
    },
    methods: {
        formatImageUrl(image_url){
            if(image_url.startsWith('http')){
                return image_url;
            }
            else{
                return this.$http.server_host+image_url;
            }
        },
        initForm(banner){
            if(banner){
                this.form.id = banner.id
                this.form.name = banner.name;
                this.form.image_url = banner.image_url;
                this.form.link_url = banner.link_url;
                this.form.priority = banner.priority;
            }
            else{
                this.form = {
                    name: "",
                    image_url: "",
                    link_url: "",
                    priority: 0
                }
            }
        },
        onAddButtonClick(){
            this.initForm();
            this.bannerDialogVisible = true;
        },
        onImageUploadSuccess(response){
            if (response['code'] == 200)
            {
                var image_name = response['data']['image_url'];
                var image_url = "/media/banner/" + image_name;
                this.form.image_url = image_url;

            }
        },
        onImageUploadError(response, uploadFile, uploadFiles){
            console.log(response);
            console.log(uploadFile);
            console.log(uploadFiles);
        },
        onDialogSubmitEvent(){
            this.$refs['dialogForm'].validate((valid) => {
                if(!valid){
                    ElMessage.error('请确保输入数据正确');
                    return;
                }
                if(this.form.id)
                {
                    this.$http.editBanner(this.form).then((result) => {
                    let code = result['code'];
                    if(code === 200){
                        let banner = result['data'];
                        // this.banners.push(banner);
                        this.banners.splice(this.editingIndex, 1, banner)
                        ElMessage.success("轮播图修改成功！")
                        this.bannerDialogVisible = false
                    }
                })
                }else{
                    this.$http.addBanner(this.form).then((result) => {
                    let code = result['code'];
                    if(code === 200){
                        let banner = result['data'];
                        this.banners.push(banner);
                        ElMessage.success("轮播图添加成功！")
                        this.bannerDialogVisible = false
                    }
                }).catch(() =>{
                    ElMessage.error("服务器开小差了~")
                })
                }
                

            })
        },
        onEditEvent(index){
            this.editingIndex = index;
            let banner = this.banners[index];
            this.initForm(banner);
            this.bannerDialogVisible = true
        },
        onDeleteEvent(index){
            this.deleteingIndex = index;
            this.deleteDialogVisible = true;
        },
        onConfirmDeleteEvent(){
            let banner = this.banners[this.deleteingIndex];
            this.$http.deleteBanner(banner.id).then(result =>{
                let code = result['code'];
                    if(code === 200){
                        this.banners.splice(this.deleteingIndex, 1);
                        ElMessage.success("轮播图已删除！");
                        this.deleteDialogVisible = false;
                    }
            })
        }
    }
  };
  </script>
  
  <style scoped>
  .el-space {
    display: block;
  }
  </style>
  
<template>
    <div class="home">
        <div class="homeBanner">
            <div class="homeBanner-title">
                <div class="homeBanner-title-left">
                    <div class="homeBanner-title-left-img">
                        <img src="../assets/images/ycy1.jpeg" alt="">
                    </div>
                    <span>全村的希望</span>
                </div>
                <div class="homeBanner-title-right">
                    <span class="fr leader-pc" @mouseenter="showQrCode" @mouseout="hideQrCode">联系负责人</span>
                    <span class="fr leader-mobile" @click="showQrCodeMobile">联系负责人</span>
                </div>
                <div class="qrCode"  ref="leaderCode">
                    <i class="iconfont icon-sanjiaoxing1"></i>
                    <img src="../assets/images/leader.png" alt="">
                </div>
            </div>
            <div class="homeBanner-content">
                <div class="homeBanner-content-left">
                    <div class="text-box">
                        <div class="whole-village-hope-pc hasAfter" >
                            全村的希望
                            <img src="../assets/images/version1.png" class="versionImg" alt="">
                        </div>
                        <h2>基于区块链技术开发</h2>
                    </div>
                    
                    <div class="homeBanner-content-left-img">
                        <img src="../assets/images/qrCode.jpeg" alt="">
                        <span>扫描与超越聊天吧</span>
                    </div>
                </div>
                <div class="homeBanner-content-right">
                    <img src="../assets/images/bannerBg.png" alt="">
                </div>
            </div>
        </div>
        <div class="introduce-text-left">
            <div class="introduce-text-left-text">
                <h2>构建「 杨超越微信生态 」的神器</h2>
                <p>不同微信群之间的积分互转、</p>
                <p>智能语聊、吸越、红包系统、超越相关小游戏</p>
                <p>......</p>
                <div class="toGitHub" ><a href="https://github.com/albertschr/ycy_wechat_robot_supported_blockchain" target="_blank" style="color: #ffffff;">前往全村的沙雕GitHub</a></div>
            </div>
            <div class="introduce-text-left-img">
                <img src="../assets/images/ycyBg1.jpg" alt="" style="width: 120%;">
            </div>
        </div>
        <div class="introduce-text-right">
            <div class="introduce-text-right-img">
                <img src="../assets/images/ycyBg2.png" alt="">
            </div>
            <div class="introduce-text-right-text">
                <h2>微信群的等级系统与积分系统</h2>
                <p>基于区块链技术的杨超越微信小助手</p>
            </div>
        </div>
        <div class="introduce-text-left">
            <div class="introduce-text-left-text">
                <h2>不同微信群之间的积分互转</h2>
                <p>不同微信群之间的积分互转、</p>
                <p>智能语聊、吸越、红包系统、超越相关小游戏</p>
                <p>......</p>
                <div class="toGitHub" ><a href="https://github.com/albertschr/ycy_wechat_robot_supported_blockchain" target="_blank" style="color: #ffffff;" >前往全村的沙雕GitHub</a></div>
            </div>
            <div class="introduce-text-left-img" style="margin-top: 30px;">
                <img src="../assets/images/ycyBg3.png" alt="">
            </div>
        </div>
        <div class="introduce-text-right">
            <div class="introduce-text-right-img">
                <img src="../assets/images/ycyBg4.png" alt="">
            </div>
            <div class="introduce-text-right-text">
                <h2>智能语聊与智能吸花</h2>
                <p>基于区块链技术的杨超越微信小助手</p>
            </div>
        </div>
        <div class="introduce-text-left">
            <div class="introduce-text-left-text">
                <h2>智能红包系统</h2>
                <p>不同微信群之间的积分互转、</p>
                <p>智能语聊、吸越、红包系统、超越相关小游戏</p>
                <p>......</p>
                <div class="toGitHub" ><a href="https://github.com/albertschr/ycy_wechat_robot_supported_blockchain" target="_blank" style="color: #ffffff;">前往全村的沙雕GitHub</a></div>
            </div>
            <div class="introduce-text-left-img" style="margin-top: 30px;">
                <img src="../assets/images/redBag.jpg" alt="">
            </div>
        </div>
        <div class="messageBoard">
            <div class="messageBoard-title">
                <h2>村民 & 月芽留言板</h2>
                <p @click="leaveMessage">我要留言</p>
            </div>
            <div class="messageBoard-content">
                <li class="item" v-for="item in messageList" :key="item.id">
                    <h3>{{item.name}}:</h3>
                    <span style="margin: 10px 0;">
                        {{item.context}}
                    </span>
                    <p class="hopeBtn">{{item.group_name}}</p>
                </li>
            </div>
        </div>
        <div class="dialogBg"  v-if="isShowDialog" @click="closeDialog"></div>
        <div class="messageDialog" v-if="isShowDialog">
            <div class="messageDialog-title">
                <span>写留言</span>
                <em class="closeDialog" @click="closeDialog"><i class="iconfont icon-searchclose"></i></em>
            </div>
            <div class="messageDialog-textarea">
                <textarea name="" id="message-textarea" v-model="iptValue" placeholder="吸花一时爽，一直吸花一直爽...">

                </textarea>
            </div>
            <div class="messageDialog-sendBtn">
                <button @click="onSubmit" style="font-size: 12px;">发送给超越</button>
            </div>

        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { Message } from 'element-ui';
    export default {
        name: 'home',
        components: {
            
        },
        data(){
            return {
                messageList: [],
                isShowDialog: false,
                iptValue: '',
                showCode: true
            }
        },
        mounted(){
            this.getMessage();
        },
        
        methods: {
            getMessage(){
                axios.get('api/v1/ycy/messages').then(res => {
                    if(200 === res.status){
                        this.messageList = res.data
                    }
                })
            },
            leaveMessage(){
                console.log('添加留言')
                this.isShowDialog = true
            },
            closeDialog(){
                this.isShowDialog = false;
                this.iptValue = ''
            },
            onSubmit(){
                axios.post('api/v1/ycy/messages/create',{
                    context: this.iptValue,
                    name: '村民',
                    group_name: '留言板'
                }).then(res => {
                    if(res.data.status === 'ok'){
                        this.$message({
                            message: '留言发布成功',
                            type: 'success'
                        });
                    }else{
                        this.$message.error('系统错误，请稍后重试');
                    }
                    this.isShowDialog = false;
                    this.iptValue = ''
                    this.getMessage();
                })
            },
            showQrCode(){
                this.$refs.leaderCode.style.opacity = '1'
            },
            hideQrCode(){
                this.$refs.leaderCode.style.opacity = '0'
            },
            showQrCodeMobile(){
                this.$refs.leaderCode.style.opacity = '1'
            }
        }
    }
</script>



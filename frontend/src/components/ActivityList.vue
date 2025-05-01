<template>
  <div class="activity-list-container">
    <div class="activity-grid">
      <el-card
        class="activity-card"
        v-for="activity in activities"
        :key="activity.id"
        @click="showActivityDetail(activity)"
      >
        <img :src="activity.image" class="activity-image" :alt="activity.title">
        <div class="activity-info">
          <h3>{{ activity.title }}</h3>
          <p>地点：{{ activity.location }}</p>
          <p>时间：{{ activity.time }}</p>
        </div>
      </el-card>
    </div>

    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedActivity ? selectedActivity.title : ''"
      width="50%"
      :before-close="() => detailDialogVisible = false"
    >
      <div v-if="selectedActivity">
        <p><strong>地点:</strong> {{ selectedActivity.location }}</p>
        <p><strong>时间:</strong> {{ selectedActivity.time }}</p>
        <p><strong>描述:</strong> {{ selectedActivity.description }}</p>
        <p><strong>详细内容:</strong></p>
        <p>{{ selectedActivity.details }}</p>

        <div class="activity-real-photos" v-if="selectedActivity">
          <h4>实景照片:</h4>
          <div class="upload-photo-section">
             <el-button size="small" @click="triggerFileUpload">上传照片</el-button>
             <input type="file" ref="fileInput" @change="handleFileUpload" multiple accept="image/*" style="display: none;">
          </div>

          <div class="photo-grid" v-if="selectedActivity.realPhotos && selectedActivity.realPhotos.length > 0">
            <img
              v-for="(photoUrl, index) in selectedActivity.realPhotos"
              :key="index"
              :src="photoUrl"
              alt="活动实景照片"
              class="real-photo-thumbnail"
            />
          </div>
           <div v-else class="no-photos-message">
              <p>暂无实景照片，快来上传第一张吧！</p>
           </div>
        </div>
        </div>
       <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button @click="openEvaluationListDialog">查看活动评价 ({{ selectedActivity?.evaluations?.length || 0 }})</el-button> <el-button @click="openEvaluationDialog">评价活动</el-button>
          <el-button @click="openRegistrationDialog">活动报名</el-button>
          <el-button type="primary" @click="openReservationDialog">立即预约</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="reservationDialogVisible"
      title="活动预约"
      width="40%"
      :before-close="() => reservationDialogVisible = false"
    >
      <el-form :model="reservationFormData" label-width="100px">
        <el-form-item label="预约活动">
          <span>{{ selectedActivity ? selectedActivity.title : '加载中...' }}</span>
        </el-form-item>
        <el-form-item label="预约日期">
          <el-date-picker
            v-model="reservationFormData.reservationDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="联系人姓名">
          <el-input v-model="reservationFormData.contactName" placeholder="请输入姓名"></el-input>
        </el-form-item>
         <el-form-item label="联系电话">
          <el-input v-model="reservationFormData.contactPhone" placeholder="请输入电话"></el-input>
        </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="reservationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReservation">提交预约</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="evaluationDialogVisible"
      title="评价活动"
      width="40%"
      :before-close="() => evaluationDialogVisible = false"
    >
       <el-form :model="evaluationFormData" label-width="100px">
         <el-form-item label="活动名称">
            <span>{{ selectedActivity ? selectedActivity.title : '加载中...' }}</span>
         </el-form-item>
         <el-form-item label="评分">
            <el-rate v-model="evaluationFormData.rating" :max="5" allow-half></el-rate>
         </el-form-item>
         <el-form-item label="评价内容">
            <el-input
                type="textarea"
                v-model="evaluationFormData.comment"
                placeholder="请输入您的评价内容"
                :rows="4"
            ></el-input>
         </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="evaluationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitEvaluation">提交评价</el-button>
        </span>
      </template>
    </el-dialog>

     <el-dialog
      v-model="evaluationListDialogVisible"
      :title="selectedActivity ? `${selectedActivity.title} 评价列表` : '活动评价列表'"
      width="50%"
      :before-close="() => evaluationListDialogVisible = false"
    >
       <div v-if="selectedActivity && selectedActivity.evaluations && selectedActivity.evaluations.length > 0">
           <el-card
               class="evaluation-card"
               v-for="evaluation in selectedActivity.evaluations"
               :key="evaluation.id"
           >
               <div class="evaluation-header">
                   <span class="user-name">{{ evaluation.userName }}</span>
                   <el-rate v-model="evaluation.rating" :max="5" disabled show-score text-color="#ff9900"></el-rate>
               </div>
               <div class="evaluation-content">{{ evaluation.comment }}</div>
               <div class="evaluation-actions">
                   <el-button link type="primary" size="small" @click="likeEvaluation(evaluation)">点赞</el-button>
                   <el-button link type="primary" size="small" @click="openCommentDialog(evaluation)">评论</el-button>
                   </div>
               </el-card>
       </div>
       <div v-else>
           <p>暂无评价。</p>
       </div>
       <template #footer>
        <span class="dialog-footer">
          <el-button @click="evaluationListDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

     <el-dialog
      v-model="registrationDialogVisible"
      title="活动报名"
      width="40%"
      :before-close="() => registrationDialogVisible = false"
    >
       <el-form :model="registrationFormData" label-width="100px">
         <el-form-item label="报名活动">
            <span>{{ selectedActivity ? selectedActivity.title : '加载中...' }}</span>
         </el-form-item>
         <el-form-item label="您的昵称">
            <el-input v-model="registrationFormData.nickname" placeholder="请输入您的昵称"></el-input>
         </el-form-item>
         <el-form-item label="联系方式">
            <el-input v-model="registrationFormData.contactInfo" placeholder="请输入您的电话或邮箱"></el-input>
         </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="registrationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRegistration">提交报名</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="commentDialogVisible"
      :title="currentEvaluationToComment ? `评论 ${currentEvaluationToComment.userName} 的评价` : '评论评价'"
      width="40%"
      :before-close="() => commentDialogVisible = false"
    >
       <div v-if="currentEvaluationToComment">
            <p>回复给：{{ currentEvaluationToComment.userName }} 的评价</p>
            <p class="original-comment">{{ currentEvaluationToComment.comment }}</p>
            <el-form :model="commentFormData" label-width="100px" style="margin-top: 20px;">
                <el-form-item label="您的评论">
                    <el-input
                        type="textarea"
                        v-model="commentFormData.commentText"
                        placeholder="请输入您的评论"
                        :rows="3"
                    ></el-input>
                </el-form-item>
            </el-form>
       </div>
       <div v-else>
           <p>加载评论信息失败。</p>
       </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="commentDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitComment">提交评论</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
// 导入所有需要的 Element Plus 组件
import {
  ElDialog,
  ElButton,
  ElMessage,
  ElForm,
  ElFormItem,
  ElInput,
  ElDatePicker,
  ElRate, // 导入评分组件
  ElCard // 导入卡片组件
} from 'element-plus';

// 示例活动数据，增加 evaluations 字段存储评价列表
const activities = ref([
  {
    id: 1,
    image: 'https://readdy.ai/api/search-image?query=organic%20vegetable%20farm%20with%20people%20picking%20vegetables%2C%20green%20fields%2C%20sunny%20day%2C%20colorful%20vegetables%2C%20people%20enjoying%20farming%20experience%2C%20high%20quality%20photorealistic&width=400&height=250&seq=4&orientation=landscape',
    title: '有机蔬菜采摘体验 - 感受自然农耕的魅力',
    location: '北京市密云区',
    time: '2025-05-01',
    description: '亲手采摘新鲜有机蔬菜，体验田园乐趣！',
    details: '本次活动将在北京市密云区的一处有机农场举行。活动内容包括农场参观、蔬菜采摘、农家午餐等。你将有机会亲手采摘当季最新鲜的有机蔬菜，了解有机种植知识，并品尝地道的农家美食。适合家庭、朋友一同参与。请注意防晒和携带防蚊用品。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=organic%20vegetable%20farm%20scene%20with%20people%20working%2C%20sunny%20day%2C%20photorealistic&width=600&height=400&seq=1',
      'https://readdy.ai/api/search-image?query=people%20picking%20vegetables%20in%20organic%20farm%2C%20close%20up%2C%20photorealistic&width=600&height=400&seq=2',
      'https://readdy.ai/api/search-image?query=freshly%20harvested%20organic%20vegetables%20in%20basket%2C%20photorealistic&width=600&height=400&seq=3'
    ],
    evaluations: [ // 添加该活动的评价列表
        { id: 101, userName: '快乐农夫', rating: 5, comment: '采摘的蔬菜很新鲜，孩子玩得很开心！' },
        { id: 102, userName: '田园爱好者', rating: 4.5, comment: '环境不错，午餐也很美味，下次还会来。' },
        { id: 103, userName: '小明同学', rating: 4, comment: '交通稍微有点远，但采摘体验很棒！' },
    ]
  },
  {
    id: 2,
    image: 'https://readdy.ai/api/search-image?query=traditional%20farming%20culture%20experience%2C%20people%20planting%20rice%20in%20paddy%20fields%2C%20plowing%20with%20traditional%20tools%2C%20beautiful%20countryside%20scenery%2C%20sunny%20day%2C%20high%20quality%20photorealistic&width=400&height=250&seq=5&orientation=landscape',
    title: '传统农耕文化体验 - 插秧、犁地、收割全流程',
    location: '河北省张家口市',
    time: '2025-05-15',
    description: '深入了解中国传统农耕文化，亲身体验农事活动。',
    details: '来到河北张家口市的乡村，参与一场原汁原味的传统农耕文化体验。活动将带你了解水稻种植的全过程，包括插秧、犁地（视季节和安排）、田间管理和模拟收割。这是一个了解“谁知盘中餐，粒粒皆辛苦”的绝佳机会。提供简易农具和指导，请准备适合劳动的衣物。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=people%20planting%20rice%20in%20paddy%20field%2C%20traditional%20way%2C%20photorealistic&width=600&height=400&seq=4',
      'https://readdy.ai/api/search-image?query=traditional%20plowing%20with%20ox%20in%20paddy%20field%2C%20photorealistic&width=600&height=400&seq=5',
      'https://readdy.ai/api/search-image?query=golden%20paddy%20fields%20harvest%20scene%2C%20people%20cutting%20rice%2C%20photorealistic&width=600&height=400&seq=6'
    ],
     evaluations: [ // 添加该活动的评价列表
        { id: 201, userName: '文化体验者', rating: 5, comment: '非常独特和有意义的体验，学到了很多农耕知识。' },
        { id: 202, userName: '家庭出游', rating: 4, comment: '孩子亲手体验了插秧，很新奇，是不错的亲子活动。' },
    ]
  },
  {
    id: 3,
    image: 'https://readdy.ai/api/search-image?query=rural%20handicraft%20making%20workshop%2C%20people%20making%20pottery%2C%20weaving%20baskets%2C%20and%20tie-dyeing%20fabrics%2C%20colorful%20materials%2C%20indoor%20workshop%20with%20natural%20light%2C%20high%20quality%20photorealistic&width=400&height=250&seq=6&orientation=landscape',
    title: '乡村手工艺制作 - 陶艺、编织、扎染',
    location: '北京市怀柔区',
    time: '2025-05-20',
    description: '体验传统手工艺制作的乐趣，带走你的专属作品。',
    details: '在北京市怀柔区的乡村工作室里，学习和体验三项传统手工艺：陶艺、竹编和扎染。专业的老师会指导你完成一件属于自己的作品。无论是亲手制作一个陶碗，编织一个小篮子，还是设计一块扎染布，都能让你感受到传统工艺的魅力。所有材料和工具均已备好。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=people%20making%20pottery%20in%20workshop%2C%20photorealistic&width=600&height=400&seq=7',
      'https://readdy.ai/api/search-image?query=person%20weaving%20bamboo%20basket%2C%20close%20up%2C%20photorealistic&width=600&height=400&seq=8',
      'https://readdy.ai/api/search-image?query=tie-dyeing%20process%2C%20colorful%20fabrics%2C%20photorealistic&width=600&height=400&seq=9'
    ],
     evaluations: [ // 添加该活动的评价列表
        { id: 301, userName: '手工达人', rating: 5, comment: '老师很专业，作品很满意，度过了充实的一天！' },
        { id: 302, userName: '周末休闲', rating: 4.5, comment: '环境很好，非常放松，扎染很有趣。' },
    ]
  },
  {
    id: 4,
    image: 'https://readdy.ai/api/search-image?query=mountain%20stream%20fishing%20experience%2C%20people%20fishing%20in%20natural%20ecological%20environment%2C%20beautiful%20mountains%20and%20clear%20water%2C%20peaceful%20atmosphere%2C%20sunny%20day%2C%20high%20quality%20photorealistic&width=400&height=250&seq=7&orientation=landscape',
    title: '山间溪流野钓体验 - 原生态环境中的放松时光',
    location: '河北省承德市',
    time: '2025-04-28',
    description: '在清澈的山间溪流享受宁静的垂钓乐趣。',
    details: '逃离城市的喧嚣，来到河北承德市的山间，体验一次纯净的溪流野钓。这里水质清澈，环境优美，是放松身心的好去处。活动包含基础钓具租赁和简单的钓鱼技巧指导。你可以享受垂钓的乐趣，呼吸新鲜空气，感受大自然的宁静。渔获可选择带走或按规定放生。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=person%20fishing%20in%20mountain%20stream%2C%20beautiful%20scenery%2C%20photorealistic&width=600&height=400&seq=10',
      'https://readdy.ai/api/search-image?query=clear%20mountain%20stream%2C%20rocks%20and%20trees%2C%20photorealistic&width=600&height=400&seq=11'
    ],
     evaluations: [ // 添加该活动的评价列表
        { id: 401, userName: '钓鱼佬', rating: 5, comment: '环境太棒了，水很清，钓到了几条小鱼，很满意！' },
        { id: 402, userName: '自然爱好者', rating: 4.5, comment: '风景很好，非常安静，适合发呆和放松。' },
    ]
  },
  {
    id: 5,
    image: 'https://readdy.ai/api/search-image?query=special%20homestay%20experience%20combining%20traditional%20and%20modern%20elements%2C%20beautiful%20countryside%20house%20with%20garden%2C%20cozy%20interior%2C%20natural%20surroundings%2C%20sunset%20time%2C%20high%20quality%20photorealistic&width=400&height=250&seq=8&orientation=landscape',
    title: '特色民宿住宿体验 - 古朴与现代的完美结合',
    location: '北京市延庆区',
    time: '2025-05-01',
    description: '入住具有当地特色的民宿，感受不一样的乡村生活。',
    details: '我们在北京市延庆区精心挑选了一处融合古朴建筑风格与现代舒适设施的特色民宿。在这里，你可以在宁静的乡村环境中放松身心，体验当地的生活节奏。民宿提供舒适的住宿环境、美味的乡村早餐，并且周围有丰富的自然景观和徒步路线。是周末短途度假的理想选择。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=countryside%20homestay%20exterior%2C%20traditional%20architecture%2C%20garden%2C%20photorealistic&width=600&height=400&seq=12',
      'https://readdy.ai/api/search-image?query=cozy%20homestay%20interior%2C%20bedroom%2C%20photorealistic&width=600&height=400&seq=13',
      'https://readdy.ai/api/search-image?query=homestay%20dining%20area%2C%20countryside%20view%2C%20photorealistic&width=600&height=400&seq=14'
    ],
    evaluations: [ // 添加该活动的评价列表
        { id: 501, userName: '度假客', rating: 5, comment: '民宿很有特色，环境幽静，非常适合放松度假。' },
        { id: 502, userName: '周末出游', rating: 4.5, comment: '房间干净舒适，早餐很棒，周围风景也好。' },
    ]
  },
  {
    id: 6,
    image: 'https://readdy.ai/api/search-image?query=rural%20cuisine%20cooking%20class%2C%20people%20learning%20to%20cook%20traditional%20farm%20dishes%2C%20kitchen%20with%20traditional%20elements%2C%20fresh%20ingredients%2C%20people%20enjoying%20cooking%20together%2C%20high%20quality%20photorealistic&width=400&height=250&seq=9&orientation=landscape',
    title: '乡村美食制作 - 传统农家菜烹饪课程',
    location: '天津市蓟州区',
    time: '2025-05-20',
    description: '学习制作地道的农家菜，品尝劳动的果实。',
    details: '来到天津市蓟州区的农家厨房，跟当地的老师傅学习制作几道经典的农家菜。从食材的选择到烹饪的技巧，你将全程参与，亲手做出美味佳肴。这是一个了解地方饮食文化、体验动手乐趣的好机会。课程结束后，大家可以一同品尝自己亲手制作的农家大餐。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=people%20cooking%20in%20traditional%20kitchen%2C%20farmhouse%20cuisine%2C%20photorealistic&width=600&height=400&seq=15',
      'https://readdy.ai/api/search-image?query=fresh%20ingredients%20for%20farmhouse%20cooking%2C%20vegetables%20and%20meat%2C%20photorealistic&width=600&height=400&seq=16',
      'https://readdy.ai/api/search-image?query=cooked%20farmhouse%20dishes%20on%20table%2C%20delicious%20food%2C%20photorealistic&width=600&height=400&seq=17'
    ],
     evaluations: [ // 添加该活动的评价列表
        { id: 601, userName: '美食家', rating: 5, comment: '学到了几道拿手农家菜，老师教得很仔细，非常实用！' },
        { id: 602, userName: '吃货', rating: 4, comment: '自己动手做的就是好吃，就是人有点多。' },
    ]
  },
   {
    id: 7,
    image: 'https://readdy.ai/api/search-image?query=strawberry%20picking%20activity%20in%20a%20greenhouse%2C%20close%20up%20of%20fresh%20red%20strawberries%20on%20plants%2C%20people%20picking%20strawberries%20in%20background%2C%20bright%20and%20clean%20environment%2C%20educational%20farming%20experience%2C%20photorealistic&width=400&height=300&seq=4&orientation=landscape',
    title: '春季草莓采摘体验',
    location: '北京市顺义区草莓园',
    time: '2025-05-01',
    description: '阳光温室草莓采摘，体验采摘乐趣，品尝新鲜美味。',
    details: '顺义区的草莓园提供高品质的温室草莓。在温暖舒适的环境中，你可以尽情采摘香甜可口的草莓。农场工作人员会指导你如何挑选和采摘。适合亲子活动和朋友聚会。采摘的草莓按重量收费。请提前预约。',
    realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=greenhouse%20strawberry%20farm%2C%20rows%20of%20strawberry%20plants%2C%20photorealistic&width=600&height=400&seq=18',
      'https://readdy.ai/api/search-image?query=child%20picking%20strawberries%20in%20greenhouse%2C%20smiling%2C%20photorealistic&width=600&height=400&seq=19',
      'https://readdy.ai/api/search-image?query=basket%20of%20freshly%20picked%20strawberries%2C%20close%20up%2C%20photorealistic&width=600&height=400&seq=20'
    ],
     evaluations: [ // 添加该活动的评价列表
        { id: 701, userName: '草莓控', rating: 5, comment: '草莓又大又甜，采摘很方便，小朋友特别喜欢！' },
        { id: 702, userName: '家庭乐', rating: 4.5, comment: '温室很干净，不怕天气影响，草莓品质很好。' },
    ]
  },
  {
    id: 8,
    image: 'https://readdy.ai/api/search-image?query=beautiful%20countryside%20homestay%20with%20traditional%20Chinese%20architecture%2C%20cozy%20bedroom%20interior%20with%20wooden%20furniture%2C%20large%20windows%20with%20mountain%20view%2C%20warm%20lighting%2C%20peaceful%20atmosphere%2C%20photorealistic&width=400&height=300&seq=5&orientation=landscape',
    title: '乡村民宿周末度假套餐',
    location: '北京市怀柔区山水间民宿',
    time: '2025-05-01',
    description: '逃离城市喧嚣，享受宁静的乡村周末，体验特色民宿。',
    details: '预订怀柔山水间民宿的周末度假套餐，包含两晚住宿和特色早餐。民宿环境优美，依山傍水，提供舒适的住宿体验和周到的服务。你可以在周边进行徒步、骑行等户外活动，或者只是在民宿里静静地阅读、品茶。这是一个放松身心、亲近自然的好机会。',
     realPhotos: [ // 示例实景照片URL
      'https://readdy.ai/api/search-image?query=traditional%20chinese%20style%20homestay%20exterior%2C%20mountain%20background%2C%20photorealistic&width=600&height=400&seq=21',
      'https://readdy.ai/api/search-image?query=cozy%20homestay%20interior%2C%20bedroom%2C%20photorealistic&width=600&height=400&seq=22',
      'https://readdy.ai/api/search-image?query=scenic%20view%20from%20homestay%20window%2C%20mountains%20and%20trees%2C%20photorealistic&width=600&height=400&seq=23'
    ],
    evaluations: [ // 添加该活动的评价列表
        { id: 801, userName: '隐居客', rating: 5, comment: '非常安静舒适的民宿，环境一流，适合放空自己。' },
        { id: 802, userName: '自然醒', rating: 4.5, comment: '早餐有当地特色，房间view很好，床品很舒服。' },
    ]
  },
]);

// 控制活动详情弹窗的显示状态
const detailDialogVisible = ref(false);
// 存储当前选中的活动对象的数据
const selectedActivity = ref(null);

// 控制预约弹窗的显示状态
const reservationDialogVisible = ref(false);

// 预约表单数据
const reservationFormData = reactive({
  reservationDate: '', // 预约日期
  contactName: '',     // 联系人姓名
  contactPhone: '',    // 联系电话
  // 你可以根据需要添加更多字段
});

// 控制评价表单弹窗的显示状态
const evaluationDialogVisible = ref(false);

// 评价表单数据
const evaluationFormData = reactive({
  rating: 0,       // 评分 (使用数字 0-5)
  comment: ''      // 评价内容
});

// 控制评价列表弹窗的显示状态
const evaluationListDialogVisible = ref(false); // 新增评价列表弹窗状态

// 控制活动报名弹窗的显示状态
const registrationDialogVisible = ref(false); // 新增活动报名弹窗状态

// 活动报名表单数据
const registrationFormData = reactive({ // 新增活动报名表单数据
  nickname: '',     // 昵称
  contactInfo: '',  // 联系方式
});

// 控制评论表单弹窗的显示状态
const commentDialogVisible = ref(false); // 新增评论表单弹窗状态

// 评论表单数据
const commentFormData = reactive({ // 新增评论表单数据
    commentText: '' // 评论内容
});

// 存储当前正在评论的评价对象
const currentEvaluationToComment = ref(null); // 新增，用于在评论弹窗中引用被评论的评价

// 文件上传 input 元素的引用
const fileInput = ref(null); // 新增，用于引用隐藏的文件输入框


// 显示活动详情弹窗的函数
const showActivityDetail = (activity) => {
  selectedActivity.value = activity; // 将点击的活动对象赋值给 selectedActivity
  detailDialogVisible.value = true; // 设置 detailDialogVisible 为 true，显示弹窗
};

// 打开预约弹窗的函数
const openReservationDialog = () => {
  // 此时 selectedActivity 已经被 showActivityDetail 设置为当前活动的详情

  // 重置预约表单数据
  Object.assign(reservationFormData, {
    reservationDate: '',
    contactName: '',
    contactPhone: '',
  });
  // 显示预约弹窗
  reservationDialogVisible.value = true;
};

// 提交预约申请的函数
const submitReservation = () => {
  console.log('提交预约数据:', {
    activityTitle: selectedActivity.value.title, // 包含活动名称
    ...reservationFormData
  });

  // 这里模拟一个提交过程，实际应用中你需要调用后端 API 发送 reservationFormData 和 selectedActivity.value.id 等数据
  // 假设提交成功
  ElMessage({
    message: '预约成功！感谢您的预约。',
    type: 'success',
  });

  // 提交成功后关闭预约弹窗
  reservationDialogVisible.value = false;

  // 可以在这里添加查看预约状态的逻辑
};


// 打开评价弹窗的函数
const openEvaluationDialog = () => {
    // 此时 selectedActivity 已经被 showActivityDetail 设置为当前活动的详情

    // 重置评价表单数据
    Object.assign(evaluationFormData, {
        rating: 0,
        comment: ''
    });
    // 显示评价弹窗
    evaluationDialogVisible.value = true;
};

// 提交评价的函数
const submitEvaluation = () => {
    console.log('提交评价数据:', {
        activityTitle: selectedActivity.value.title, // 包含活动名称
        ...evaluationFormData
    });

    // 这里模拟一个提交过程，实际应用中你需要调用后端 API 提交评价到后端
    // 假设提交成功
     ElMessage({
        message: '评价提交成功！感谢您的反馈。',
        type: 'success',
    });

    // 提交成功后关闭评价弹窗
    evaluationDialogVisible.value = false;

    // 实际应用中，这里应该调用 API 提交评价到后端，并在成功后刷新该活动的评价列表
    // 为了演示，我们在这里不进行实际刷新，但你可以在这里考虑调用 openEvaluationListDialog()
};

// 打开评价列表弹窗的函数
const openEvaluationListDialog = () => {
    // 此时 selectedActivity 已经被 showActivityDetail 设置为当前活动的详情
    // 直接显示评价列表弹窗即可
    evaluationListDialogVisible.value = true;
};

// 打开活动报名弹窗的函数
const openRegistrationDialog = () => {
  // 此时 selectedActivity 已经被 showActivityDetail 设置为当前活动的详情

  // 重置报名表单数据
  Object.assign(registrationFormData, {
    nickname: '',
    contactInfo: '',
  });
  // 显示报名弹窗
  registrationDialogVisible.value = true;
};

// 提交活动报名的函数
const submitRegistration = () => {
  console.log('提交报名数据:', {
    activityTitle: selectedActivity.value.title, // 包含活动名称
    ...registrationFormData
  });

  // 这里模拟一个提交过程，实际应用中你需要调用后端 API 提交报名信息
  // 假设提交成功
   ElMessage({
    message: '报名成功！',
    type: 'success',
  });

  // 提交成功后关闭报名弹窗
  registrationDialogVisible.value = false;

  // 可以在这里添加其他后续操作，例如提示用户等待审核等
};

// 处理点赞评价的函数
const likeEvaluation = (evaluation) => {
    console.log('点赞评价:', evaluation.id, ' 来自活动:', selectedActivity.value.title);
    // 实际应用中，这里应该调用后端 API 记录点赞，并更新评价的点赞数量
    ElMessage({
        message: `您点赞了 ${evaluation.userName} 的评价！`,
        type: 'success',
        duration: 1500 // 短暂显示
    });
    // 如果需要在前端显示点赞数量，evaluation数据结构需要增加一个likes字段，并在点击时更新它
    // evaluation.likes = (evaluation.likes || 0) + 1; // 示例更新方式
};

// 打开评论弹窗的函数
const openCommentDialog = (evaluation) => {
    currentEvaluationToComment.value = evaluation; // 记录当前要评论的评价对象
    commentFormData.commentText = ''; // 重置评论内容
    commentDialogVisible.value = true; // 显示评论弹窗
};

// 提交评论的函数
const submitComment = () => {
    if (!commentFormData.commentText.trim()) {
        ElMessage({
            message: '评论内容不能为空！',
            type: 'warning',
        });
        return;
    }

    console.log('提交评论:', {
        activityTitle: selectedActivity.value.title,
        evaluationId: currentEvaluationToComment.value.id,
        evaluationUser: currentEvaluationToComment.value.userName,
        comment: commentFormData.commentText
    });

    // 实际应用中，这里应该调用后端 API 提交评论
    // 假设提交成功
    ElMessage({
        message: '评论提交成功！',
        type: 'success',
    });

    // 提交成功后关闭评论弹窗
    commentDialogVisible.value = false;

    // 实际应用中，成功提交评论后可能需要刷新评价列表或在当前评价下方添加新评论
};

// 触发文件上传input点击的函数
const triggerFileUpload = () => { // 新增函数
  if (fileInput.value) {
    fileInput.value.click();
  }
};

// 处理文件上传的函数
const handleFileUpload = (event) => { // 新增函数
  const files = event.target.files;
  if (!files || files.length === 0) {
    return;
  }

  // 确保 selectedActivity 存在并且 realPhotos 是一个数组
  if (!selectedActivity.value) {
      ElMessage({ message: '请先选择一个活动！', type: 'warning' });
      event.target.value = ''; // 清空文件输入框
      return;
  }
   if (!selectedActivity.value.realPhotos) {
      selectedActivity.value.realPhotos = []; // 如果不存在则初始化
   }

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    if (!file.type.startsWith('image/')) {
        ElMessage({ message: `文件 ${file.name} 不是图片格式！`, type: 'warning' });
        continue; // 跳过非图片文件
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      // 将读取到的 data URL 添加到当前活动的实景照片列表中 (前端模拟显示)
      selectedActivity.value.realPhotos.push(e.target.result);
    };
    reader.readAsDataURL(file); // 以 Data URL 格式读取文件
  }

   ElMessage({
        message: `成功上传了 ${files.length} 张照片！`,
        type: 'success',
    });

  // 清空文件输入框的值，以便再次选择相同的文件也能触发 change 事件
  event.target.value = '';
};


// 注意：如果你需要从 API 获取活动数据，请保留或添加 onMounted 钩子
// import touristApiService from './services/touristApi';
// import { onMounted } from 'vue';
// onMounted(async () => {
//   try {
//     // 假设你的 API 返回的活动数据包含了 description, details, realPhotos, evaluations 等字段
//     activities.value = await touristApiService.getActivities();
//   } catch (error) {
//     console.error('获取活动数据失败:', error);
//   }
// });

</script>

<style scoped>
/* activity-list-container 和 activity-grid 的样式 */
.activity-list-container {
  padding: 20px 0;
}

.activity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

/* activity-card 样式 */
.activity-card {
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 0;
  cursor: pointer; /* 添加光标样式，表示可点击 */
}

.activity-image {
  width: 100%;
  display: block;
  object-fit: cover;
  height: 200px;
}

.activity-info {
  padding: 15px;
}

.activity-info h3 {
  margin-top: 0;
  margin-bottom: 5px;
  font-size: 1.1em;
}

.activity-info p {
  margin-bottom: 5px;
  color: #555;
  font-size: 0.9em;
}

/* 弹窗内容区域的基本样式 */
.el-dialog__body {
  padding: 20px;
  line-height: 1.6;
}

.el-dialog__body strong {
    margin-right: 5px;
}

/* 弹窗底部按钮区域的样式 */
.dialog-footer {
  text-align: right;
  /* 使用 flexbox 来控制按钮间距更灵活，并保持靠右 */
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px; /* 按钮之间的间隙 */
}

/* 实景照片区域的样式 */
.activity-real-photos {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.activity-real-photos h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 1em;
  color: #333;
}

/* 上传照片按钮区域样式 */
.upload-photo-section {
    margin-bottom: 15px;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
}

.real-photo-thumbnail {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  border-radius: 4px;
  /* cursor: pointer; 如果不需要点击图片查看大图，可以取消 */
}

.no-photos-message {
    color: #999;
    text-align: center;
    padding: 20px 0;
}


/* 评价列表卡片样式 */
.evaluation-card {
    margin-bottom: 15px; /* 评价卡片之间的间距 */
    padding: 15px;
    border-radius: 8px; /* 卡片圆角 */
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 卡片阴影 */
}

.evaluation-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.user-name {
    font-weight: bold;
    margin-right: 15px;
    color: #333;
    font-size: 1em;
}

.evaluation-content {
    color: #555;
    line-height: 1.5;
    margin-bottom: 10px; /* 内容和操作按钮之间的间距 */
}

.evaluation-actions {
    text-align: right; /* 操作按钮靠右对齐 */
}

.evaluation-actions .el-button {
    margin-left: 15px; /* 点赞和评论按钮之间的间距 */
}


/* 调整 ElRate 在评价列表中的显示 */
.el-rate {
    --el-rate-icon-size: 16px; /* 调整星星大小 */
    margin-right: 5px; /* 星星和分数之间的间距 */
}

/* 评论弹窗中显示原始评论的样式 */
.original-comment {
    font-size: 0.9em;
    color: #888;
    border-left: 3px solid #eee;
    padding-left: 10px;
    margin-bottom: 15px;
    font-style: italic; /* 斜体 */
}
</style>
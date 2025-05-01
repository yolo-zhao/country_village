<template>
  <div class="product-list-container">
    <div class="product-grid">
      <el-card
        class="product-card"
        v-for="product in products"
        :key="product.id"
        @click="showProductDetail(product)"
      >
        <img :src="product.image" class="product-image" :alt="product.name">
        <div class="product-info">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <div class="product-price">单价：￥{{ product.price }}</div>
          </div>
      </el-card>
    </div>

    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedProduct ? selectedProduct.name : ''"
      width="50%"
      :before-close="() => detailDialogVisible = false"
    >
      <div v-if="selectedProduct">
        <p><strong>商品名称:</strong> {{ selectedProduct.name }}</p>
        <p><strong>描述:</strong> {{ selectedProduct.description }}</p>
        <p><strong>单价:</strong> ￥{{ selectedProduct.price }}</p>
        <p><strong>详细介绍:</strong></p>
        <p>{{ selectedProduct.details }}</p>
        <div style="margin-top: 20px; text-align: right;">
             <el-button type="primary" size="small" @click="openConsultationDialog">咨询</el-button>
             </div>
      </div>
       <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="consultationDialogVisible"
      title="商品咨询"
      width="40%"
      :before-close="() => consultationDialogVisible = false"
    >
       <el-form :model="consultationFormData" label-width="100px">
        <el-form-item label="咨询商品">
          <span>{{ selectedProduct ? selectedProduct.name : '加载中...' }}</span>
        </el-form-item>
        <el-form-item label="您的姓名">
          <el-input v-model="consultationFormData.contactName" placeholder="请输入您的姓名"></el-input>
        </el-form-item>
         <el-form-item label="联系方式">
          <el-input v-model="consultationFormData.contactInfo" placeholder="请输入您的电话或邮箱"></el-input>
        </el-form-item>
         <el-form-item label="留言内容">
          <el-input
            type="textarea"
            v-model="consultationFormData.message"
            placeholder="请输入您想咨询的内容"
            :rows="4"
          ></el-input>
        </el-form-item>
        </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="consultationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitConsultation">提交</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElDialog, ElButton, ElMessage, ElForm, ElFormItem, ElInput } from 'element-plus'; // 确保导入所需的 Element Plus 组件

// 示例商品数据，共十个商品，每个都有唯一的ID和详细介绍 (details 字段)
const products = ref([
  {
    id: 1,
    image: 'https://readdy.ai/api/search-image?query=organic%20fresh%20vegetable%20gift%20box%20with%20seasonal%20vegetables%2C%20beautifully%20arranged%20in%20wooden%20box%2C%20vibrant%20colors%2C%20clean%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=10&orientation=landscape',
    name: '蔬菜礼盒',
    description: '有机新鲜蔬菜礼盒 - 当季时令蔬菜直送',
    price: 168.00,
    details: '精选当季最新鲜的有机认证蔬菜，直接从田间采摘后打包。礼盒内含多种蔬菜组合，确保营养均衡。无农药残留，口感鲜脆，是健康家庭的首选。每周新鲜配送。礼盒重量约3公斤。'
  },
   {
    id: 2, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=free%20range%20mountain%20chicken%20eggs%2C%2030%20eggs%20package%2C%20natural%20brown%20eggs%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=11&orientation=landscape',
    name: '土鸡蛋',
    description: '山地散养土鸡蛋 - 30枚装',
    price: 98.00,
    details: '我们的山地散养土鸡蛋来自纯天然环境下的快乐土鸡。鸡只在山间自由觅食，辅以五谷杂粮，产出的鸡蛋蛋黄饱满，蛋清浓稠，营养丰富，口感纯正。30枚精美包装，送礼自用两相宜。保质期为常温下15天，冷藏可延长。'
  },
  {
    id: 3, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=handmade%20pickled%20vegetables%20in%20glass%20jar%2C%20traditional%20craftsmanship%2C%20colorful%20vegetables%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=12&orientation=landscape',
    name: '手工泡菜',
    description: '手工腌制泡菜 - 传统工艺',
    price: 58.00,
    details: '采用当地新鲜时令蔬菜，遵循古法手工腌制。不添加任何防腐剂和人工色素，自然发酵，味道酸辣可口，清脆爽口。无论是搭配米饭、面条还是作为开胃小菜，都是极佳的选择。净含量500克。'
  },
  {
    id: 4, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=rural%20honey%20gift%20box%20with%20different%20types%20of%20flower%20honey%2C%20glass%20jars%20with%20honey%2C%20elegant%20packaging%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=200&seq=14&orientation=landscape',
    name: '百花蜜礼盒',
    description: '乡村蜂蜜礼盒 - 百花蜜组合',
    price: 199.00,
    details: '精选乡村天然蜜源，采集多种花卉精华酿制而成。口感香甜，带有独特的花草芳香，营养价值高。礼盒包含3瓶不同花源的百花蜜小瓶组合（每瓶250克），是馈赠亲友的健康好礼。'
  },
   {
    id: 5, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=premium%20organic%20strawberry%20gift%20box%20with%20fresh%20red%20strawberries%20arranged%20neatly%2C%20elegant%20packaging%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=10&orientation=squarish',
    name: '有机草莓礼盒',
    description: '精选优质草莓，无农药，口感甜美多汁',
    price: 68.00,
    details: '我们的有机草莓在严格控制的有机环境下生长，未使用任何化学农药和化肥。果实饱满，色泽鲜红，口感细腻多汁，香气浓郁。每一颗都经过精心挑选，保证品质。礼盒净含量500克。请收到后尽快食用或冷藏。'
  },
  {
    id: 6, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=artisanal%20honey%20gift%20set%20with%20glass%20jars%20of%20different%20honey%20varieties%2C%20wooden%20packaging%2C%20honeycomb%20decoration%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=11&orientation=squarish',
    name: '手工蜂蜜礼盒',
    description: '纯天然野生蜂蜜，无添加，滋养健康',
    price: 128.00,
    details: '这款手工蜂蜜礼盒包含多种珍贵的野生蜂蜜，由经验丰富的蜂农手工采集和灌装。蜂蜜未经高温处理，完整保留天然酶和营养物质。风味各异，每一款都是大自然的馈赠，具有良好的滋养和保健作用。礼盒包含2瓶不同风味蜂蜜（每瓶300克）。'
  },
  {
    id: 7, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=traditional%20Chinese%20homemade%20sausages%20hanging%20to%20dry%2C%20artisanal%20food%20product%2C%20rustic%20presentation%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=12&orientation=squarish',
    name: '农家自制腊肠',
    description: '传统工艺制作，肉质鲜美，风味独特',
    price: 98.00,
    details: '沿用世代相传的农家传统工艺制作，选用新鲜猪肉和天然调料，经过多道工序精心腌制、灌制和自然晾晒。口感紧实，肉质鲜美，带有独特的烟熏风味。无任何人工添加，是餐桌上的美味佳肴。净含量500克。建议蒸煮或煎炒后食用。'
  },
  {
    id: 8, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=handcrafted%20bamboo%20basket%20with%20intricate%20weaving%20pattern%2C%20traditional%20Chinese%20craftsmanship%2C%20elegant%20design%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=13&orientation=squarish',
    name: '手工编织竹篮',
    description: '传统手工艺品，实用美观，环保耐用',
    price: 56.00,
    details: '由经验丰富的匠人采用优质竹材，纯手工精心编织而成。纹理细腻，结构牢固，透气性好。既可以作为日常收纳、购物提篮，也是一件充满艺术气息的家居装饰品。体现了传统竹编工艺的精髓。尺寸约：直径25cm，高15cm。'
  },
  {
    id: 9, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=handmade%20soap%20gift%20set%20with%20various%20natural%20soaps%2C%20herbal%20ingredients%20visible%2C%20elegant%20packaging%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=14&orientation=squarish',
    name: '乡村手工皂礼盒',
    description: '天然植物精油制作，温和不刺激',
    price: 88.00,
    details: '采用天然植物油和精油，遵循冷制法手工制作。不含化学添加剂，温和亲肤，泡沫细腻丰富。多种不同配方，针对不同肤质需求，洗后不干燥不紧绷。精美礼盒包装，包含4块不同香味手工皂（每块约80克），是天然健康的洗护选择。'
  },
  {
    id: 6, // 确保ID唯一
    image: 'https://readdy.ai/api/search-image?query=artisanal%20honey%20gift%20set%20with%20glass%20jars%20of%20different%20honey%20varieties%2C%20wooden%20packaging%2C%20honeycomb%20decoration%2C%20clean%20white%20background%2C%20high%20quality%20product%20photography%2C%20photorealistic&width=300&height=300&seq=11&orientation=squarish',
    name: '手工蜂蜜礼盒',
    description: '纯天然野生蜂蜜，无添加，滋养健康',
    price: 128.00,
    details: '这款手工蜂蜜礼盒包含多种珍贵的野生蜂蜜，由经验丰富的蜂农手工采集和灌装。蜂蜜未经高温处理，完整保留天然酶和营养物质。风味各异，每一款都是大自然的馈赠，具有良好的滋养和保健作用。礼盒包含2瓶不同风味蜂蜜（每瓶300克）。'
  },
]);


// 控制商品详情弹窗的显示状态
const detailDialogVisible = ref(false);
// 存储当前选中的商品对象的数据
const selectedProduct = ref(null);

// 控制咨询弹窗的显示状态
const consultationDialogVisible = ref(false);

// 咨询表单数据
const consultationFormData = reactive({
  contactName: '',     // 联系人姓名
  contactInfo: '',     // 联系方式 (电话/邮箱等)
  message: ''          // 留言内容
});


// 显示商品详情弹窗的函数
const showProductDetail = (product) => {
  selectedProduct.value = product; // 将点击的商品对象赋值给 selectedProduct
  detailDialogVisible.value = true; // 设置 detailDialogVisible 为 true，显示弹窗
};

// 打开咨询弹窗的函数
const openConsultationDialog = () => {
  // 此时 selectedProduct 已经被 showProductDetail 设置为当前商品的详情

  // 重置咨询表单数据
  Object.assign(consultationFormData, {
    contactName: '',
    contactInfo: '',
    message: '',
  });
  // 显示咨询弹窗
  consultationDialogVisible.value = true;
};

// 提交咨询的函数
const submitConsultation = () => {
  console.log('提交咨询数据:', {
    productName: selectedProduct.value.name, // 包含商品名称
    ...consultationFormData
  });

  // 这里模拟一个提交过程，实际应用中你需要调用后端 API 发送 consultationFormData 和 selectedProduct.value.id 等数据
  // 假设提交成功
  ElMessage({
    message: '咨询提交成功！我们会尽快与您联系。',
    type: 'success',
  });

  // 提交成功后关闭咨询弹窗
  consultationDialogVisible.value = false;

  // 可以在这里添加其他后续操作
};


// 注意：如果你需要从 API 获取商品数据，请保留或添加 onMounted 钩子
// import touristApiService from './services/touristApi';
// import { onMounted } from 'vue';
// onMounted(async () => {
//   try {
//     // 假设你的 API 返回的商品数据包含了 details 字段
//     products.value = await touristApiService.getProducts();
//   } catch (error) {
//     console.error('获取商品数据失败:', error);
//   }
// });

</script>

<style scoped>
/* product-list-container 和 product-grid 的样式 */
.product-list-container {
  padding: 20px 0;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

/* product-card 样式 */
.product-card {
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 0;
  cursor: pointer; /* 添加光标样式，表示可点击 */
}

.product-image {
  width: 100%;
  display: block;
  object-fit: cover;
  height: 180px;
}

.product-info {
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-info h3 {
  margin-top: 0;
  margin-bottom: 0;
  font-size: 1.1em;
}

.product-price {
  color: #ff6700;
  font-weight: bold;
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
}

/* 如果需要，可以为咨询表单的输入框或文本域添加特定样式 */
/* 例如：
.el-form-item__content .el-input,
.el-form-item__content .el-textarea {
  width: 100%;
}
*/
</style>
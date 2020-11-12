<template>
  <div>
    <i
      class="fa fa-plus"
      style="float: right; margin: 0 4px; color: green"
      @click="createMetadata"
    />

    <p class="title" style="margin: 0">{{ title }}</p>

    <div class="row">
      <div class="col-sm">
        <p class="subtitle">{{ keyTitle }}</p>
      </div>
      <div class="col-sm">
        <p class="subtitle">{{ valueTitle }}</p>
      </div>
    </div>

     <div class="row">
      <div class="col-sm">
        <label>Type</label>
      </div>
      <div class="col-sm">
        <select v-model="annotationType">
          <option disabled value="">Please select one</option> 
          <option>Rectangle</option> 
          <option>Circle</option> 
          <option>Polygon</option> 
        </select>
        <i class="fa fa-plus" 
           style="float: right; margin: 0 4px; color: green"
           @click="changeAnnotationType" 
        />
      </div>
    </div>

    <div class="row">
      <div class="col-sm">
        <label>DefectCode {{ categoryName }}</label>
      </div>
      <div class="col-sm">
        <select v-model="defect_code">
          <option disabled value="">Please select one</option> 
          <option v-for="defectCode in getDefectCodeList">{{defectCode}}</option> 
        </select>
        <i class="fa fa-plus" 
           style="float: right; margin: 0 4px; color: green" 
           @click="changeDefectCode"
        />
      </div>
    </div>

    <ul class="list-group" style="height: 50%;">
      <li v-if="metadataList.length == 0" class="list-group-item meta-item">
        <i class="subtitle">No items in metadata.</i>
      </li>

     <li
        v-for="(object, index) in getMetadataList"
        :key="index"
        class="list-group-item meta-item">
        <div class="row" style="cell">
          <div class="col-sm">
            <p>{{ object.key }}</p>
            
          </div>

          <div class="col-sm">
            <p>{{ object.value }}</p>
          </div>
        </div>
      </li>


    </ul>
  </div>
</template>

<script>

import MetadataType from "@/models/metadataType";

export default {
  name: "Metadata",
  props: {
    categoryId: {

    },
    categoryName: {
      type: String
    },
    annotationId: {
      //required: true
    },
    metadata: {
      type: Object,
      required: true
    },
    title: {
      type: String,
      default: "Metadata"
    },
    keyTitle: {
      type: String,
      default: "Keys"
    },
    valueTitle: {
      type: String,
      default: "Values"
    },
    exclude: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      metadataList: [],
      defect_code: "",
      annotationType: "",
      TYPE_KEY: MetadataType.TYPE,
      CLASS_KEY: MetadataType.CLASS
    };
  },
  methods: {
    export() {
      let metadata = {};

      this.metadataList.forEach(object => {
        if (object.key.length > 0) {
          if (!isNaN(object.value))
            metadata[object.key] = parseInt(object.value);
          else if (
            object.value.toLowerCase() === "true" ||
            object.value.toLowerCase() === "false"
          )
            metadata[object.key] = object.value.toLowerCase() === "true";
          else metadata[object.key] = object.value;
        }
      });

      return metadata;
    },
    createMetadata() {
      this.metadataList.push({ key: "", value: "" });
    },
    loadMetadata() {
      this.metadataList = [];
      if (this.metadata != null) {
        for (var key in this.metadata) {
          if (!this.metadata.hasOwnProperty(key)) continue;
          if (key === this.exclude) continue;

          let value = this.metadata[key];

          if (value == null) value = "";
          else value = value.toString();
          this.metadataList.push({ key: key, value: value });
        }
      }
    },
    changeAnnotationType() {
      if (this.annotationType === "")
        return
      this.replaceMetadataWith(this.TYPE_KEY, { key: this.TYPE_KEY, value: this.annotationType });
    },
    changeDefectCode() {
      if (this.defect_code === "")
        return 
        
      this.replaceMetadataWith(this.CLASS_KEY, { key: this.CLASS_KEY, value: this.defect_code });
    },
    replaceMetadataWith(keyValue, newMetada) {
      let newMetadaList = this.removeMetadataBy(keyValue)
      newMetadaList.push(newMetada);
      this.metadataList = newMetadaList
    },
    removeMetadataBy(keyValue) {
      return this.metadataList.filter(metadata => metadata.key !== keyValue)
    }
  },
  computed: {
    getMetadataList() {
      return this.metadataList.filter(m => m.key === this.TYPE_KEY || m.key === this.CLASS_KEY)
    },
    getDefectCodeList() {
      return this.$store.getters.getDefectCodeList(this.categoryName);
    },
    getCategories() {
      return this.$store.getters.getCategories;
    }
  },
  watch: {
    metadata: {
        handler(val){
          console.log('metadata update');
          this.loadMetadata();
        },
        deep: true
    }
  },
  created() {
    this.loadMetadata();
  }
};
</script>

<style scoped>
.meta-input {
  padding: 3px;
  background-color: inherit;
  width: 100%;
  height: 100%;
  border: none;
}

.meta-item {
  background-color: inherit;
  height: 30px;
  border: none;
}

.subtitle {
  margin: 0;
  font-size: 10px;
}
</style>

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
      <li v-if="getMetadataList().length == 0" class="list-group-item meta-item">
        <i class="subtitle">No items in metadata.</i>
      </li>

     <li
        v-for="(object, index) in getDisplayMetadata"
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
      defect_code: "",
      annotationType: "",
      TYPE_KEY: MetadataType.TYPE,
      CLASS_KEY: MetadataType.CLASS
    };
  },
  methods: {
    metadataString() {
      let string = "";
      let metadata = this.getMetadataList();
      if (metadata == null || metadata.length === 0) {
        string += "No Metadata \n";
      } else {
        string += "Metadata \n";
        metadata.forEach(element => {
          if (element.key == this.TYPE_KEY || element.key == this.CLASS_KEY) {
            string += " " + element.key + " = " + element.value + " \n";
          }
        });
      }
      return string.replace(/\n/g, " \n ").slice(0, -2);
    },
    export() {
      let metadata = {};
      this.getMetadataList().forEach(object => {
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
    },
    changeAnnotationType() {
    },
    changeDefectCode() {
    },
    getMetadataList() {
      let result = [];
      if (this.metadata != null) {
        for (var key in this.metadata) {
          if (!this.metadata.hasOwnProperty(key)) continue;
          if (key === this.exclude) continue;

          let value = this.metadata[key];

          if (value == null) value = "";
          else value = value.toString();
          result.push({ key: key, value: value });
        }
      }
      return result;
    }
  },
  computed: {
    getDisplayMetadata() {
      return this.getMetadataList().filter(m => m.key === this.TYPE_KEY || m.key === this.CLASS_KEY)
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
        },
        deep: true
    }
  },
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

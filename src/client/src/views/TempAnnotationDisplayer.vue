<template>
  <div>
    <div class="row" v-if="containsTempAnnotation">
        <div class="col-sm">
          <label>Temp Annotation</label>
          <div v-for="(annotation) in getTempAnnotations" :key="annotation.id">
            <input type="checkbox" v-model="addedAnnotationIdList" :value="annotation.id"/>
            <label>{{ annotation.id }}</label>
          </div>
        </div>

        <div class="col-sm">
          <button class="change-btn" @click="saveAddedAnnotation">Save</button>
        </div>
        <hr>
    </div> 
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "TempAnnotationDisplayer",
  data() {
      return {
        addedAnnotationIdList: []
      }
  },
  methods: {
    saveAddedAnnotation() {
      this.$store.dispatch('saveTempAnnotations', this.addedAnnotationIdList);
    }
  },
  computed: {
    ...mapGetters([
      'containsTempAnnotation', 
      'getTempAnnotations'
      ]),
  }
};
</script>

<style scoped>
select {
  width: 200px;
  border: 0;  
  border: 2px solid green;
  padding: 5px;
}

label {
  margin-top: 5px;
  color: white;
}
input {
  width: 80%;
  background: transparent;
  
  padding: 5px;
  margin-top: 5px;
  border-radius: 4px;
  color: white;
  border: 0;
  border-bottom: 2px solid #9b9b9b;
}

button {
  margin-top: 5px;
  cursor: pointer;
  text-align: center;
  padding: 5px 10px;
  border-radius: 4px;
  color: white;
  border: 0;
}

.change-btn {
  background-color: green;
  margin-right: 5px;
}

button:hover {
  color: red;
}

.delete-btn {
  background-color: red;

}
</style>

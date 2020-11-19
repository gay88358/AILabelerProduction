<template>
  <div>
    <div class="row" v-if="hasAnnotationSelected">
        <div class="col-sm">
          <label>DefectCode</label>
          <select v-model="defectCode">
            <option disabled value="">Please select one</option> 
            <option v-for="defectCode in getDefectCodeOfSelectedAnnotation">{{defectCode}}</option> 
          </select>

          <input :value="getSelectedAnnotation.Type"></input>
          <input :value="getSelectedAnnotation.Class"></input>
        </div>

        <div class="col-sm">
          <button class="change-btn" @click="updateAnnotationMetadata">Change</button>
          <!--<button class="delete-btn" @click="deleteAnnotation">Delete</button>-->
        </div>
        <hr>
    </div> 
  </div>
</template>


<script>

import { mapGetters } from "vuex";

export default {
  name: "MetadataDisplayer",
  data() {
      return {
          defectCode: ""
      }
  },
  methods: {
      deleteAnnotation() {
        this.$store.dispatch(
          'deleteSelectedAnnotation'
        );
      },
      updateAnnotationMetadata() {
          this.$store.dispatch(
            'updateAnnotationMetadata', 
            {
              annotationClass: this.defectCode
            }
          );

          this.notifyAnnotationUpdated();
          this.clearDropdwonContent();
      },
      notifyAnnotationUpdated() {
          EventBus.$emit(
              "selectedAnnotationUpdate", 
              {}
          );
      },
      clearDropdwonContent() {
        this.defectCode = "";
      }
  },
  computed: {
    ...mapGetters([
      'getSelectedAnnotation', 
      'hasAnnotationSelected', 
      'getDefectCodeOfSelectedAnnotation'
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

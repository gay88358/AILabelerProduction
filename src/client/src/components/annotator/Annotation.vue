<template>
  <div
    @mouseenter="onMouseEnter"
    @mouseleave="onMouseLeave"
  >
    <li
      v-show="showSideMenu"
      class="list-group-item btn btn-link btn-sm text-left"
      :style="{ 'background-color': backgroundColor, color: 'white' }"
    >
      <div @click="isVisible = !isVisible">
        <i
          v-if="isVisible"
          class="fa fa-eye annotation-icon"
          :style="{ float: 'left', 'padding-right': '10px', color: getAnnotationColor() }"
        />
        <i
          v-else
          class="fa fa-eye-slash annotation-icon"
          style="float: left; padding-right: 10px; color: gray"
        />
      </div>

      <button
          class="btn btn-sm btn-link collapsed text-left annotation-text"
          :style="{
            float: 'left',
            width: '70%',
            color: isVisible ? 'white' : 'gray'
          }"
          aria-expanded="false"
          :aria-controls="'collapse_keypoints' + annotation.id"
          @click="onAnnotationClick(!showKeypoints);"
        >
        <template v-if="name.length === 0">
          {{ index + 1 }}
        </template>
        <template v-else> {{ name }} </template>
        {{ annotation.name }}
        <i v-if="isAnnotationNotContainsKeypoints" style="padding-left: 5px; color: lightgray"
          >(Empty)</i
        >
        <i v-else style="padding-left: 5px; color: lightgray"
          >(id: {{ annotation.id }})</i
        >
        </button>

      <i
        class="fa fa-gear annotation-icon"
        style="float:right"
        data-toggle="modal"
        :data-target="'#annotationSettings' + annotation.id"
      />
      <i
        @click="deleteAnnotation"
        class="fa fa-trash-o annotation-icon"
        style="float:right"
      />
    </li>

    <ul v-show="showKeypoints" ref="collapse_keypoints"
        class="list-group keypoint-list">
      <li v-for="(kp, index) in keypointListView" :key="index"
          :style="{'background-color': kp.backgroundColor}"
          class="list-group-item text-left keypoint-item">
        <div>
          <i class="fa fa-map-marker keypoint-icon"
              :style="{ color: kp.iconColor}"
              />
        </div>
        <a
          @click="onAnnotationKeypointClick(index)"
          :style="{
            float: 'left',
            width: '70%',
            color: 'white'
          }"
        >
          <span> {{ kp.label }} </span> 
        </a>
        <i
          v-if="kp.visibility !== 0"
          @click="onAnnotationKeypointSettingsClick(index)"
          class="fa fa-gear annotation-icon"
          style="float:right; color: lightgray;"
          data-toggle="modal"
          :data-target="'#keypointSettings' + annotation.id"
        />
        <i
          v-if="kp.visibility !== 0"
          @click="onDeleteKeypointClick(index)"
          class="fa fa-trash-o annotation-icon"
          style="float:right; color: lightgray;"
        />
      </li>
    </ul>

    <div
      class="modal fade"
      tabindex="-1"
      role="dialog"
      :id="'keypointSettings' + annotation.id"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ getKeypointLabel(currentKeypoint) }}
            </h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group row">
                <label class="col-sm-3 col-form-label">Visibility</label>
                <div class="col-sm-8">
                  <select v-model="keypoint.visibility" class="form-control">
                    <option v-for="(desc, label) in visibilityOptions" 
                      :key="label" :value="label" :selected="keypoint.visibility == label">{{desc}}</option>
                  </select>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      tabindex="-1"
      role="dialog"
      :id="'annotationSettings' + annotation.id"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ index + 1 }}
              <i style="color: darkgray">(id: {{ annotation.id }})</i>
            </h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group row">
                <label class="col-sm-3 col-form-label">Color</label>
                <div class="col-sm-8">
                  <input v-model="color" type="color" class="form-control" />
                </div>
              </div>
              <div class="form-group row">
                <label class="col-sm-3 col-form-label">Name</label>
                <div class="col-sm-8">
                  <input v-model="name" class="form-control" />
                </div>
              </div>
              <div class="form-group row">
                <label class="col-sm-3 col-form-label">Category</label>
                <div class="col-sm-8">
                  <select class="form-control" @change="setCategory">
                    <option
                      v-for="option in allCategories"
                      :selected="annotation.category_id === option.value"
                      :key="option.text"
                    >
                      {{ option.text }}
                    </option>
                  </select>
                </div>
              </div>
              <Metadata
                :categoryId="annotation.category_id"
                :metadata="annotation.metadata"
                :categoryName="categoryName"
                :annotationId="annotation.id"
                ref="metadata"
                exclude="name"
              />
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import paper from "paper";
import axios from "axios";
import JQuery from "jquery";
import { setSelectedAnnotation } from "../../models/actionDispatcher";
import { Keypoint, Keypoints, VisibilityOptions } from "@/libs/keypoints";
import { mapMutations } from "vuex";
import { keypointsRecord } from "./keypointsRecord";
import UndoAction from "@/undo";
import TagsInput from "@/components/TagsInput";
import Metadata from "@/components/Metadata";
import { CompoundPathBuilder, compoundPathRecord } from './compoundPathRecord';
import { singleAnnotationRecord } from './singleAnnotationRecord';

let $ = JQuery;

export default {
  name: "Annotation",
  components: {
    Metadata,
    TagsInput
  },
  props: {
    categoryName: {
      type: String,
      required: true
    },
    annotation: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    },
    current: {
      type: Number,
      required: true
    },
    hover: {
      type: Number,
      required: true
    },
    opacity: {
      type: Number,
      required: true
    },
    scale: {
      type: Number,
      default: 1
    },
    search: {
      type: String,
      default: ""
    },
    simplify: {
      type: Number,
      default: 1
    },
    keypointEdges: {
      type: Array,
      required: true
    },
    keypointLabels: {
      type: Array,
      required: true
    },
    keypointColors: {
      type: Array,
      required: true
    },
    activeTool: {
      type: String,
      required: true
    },
    allCategories: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      singleAnnotationRecord: singleAnnotationRecord,
      keypointsRecord: keypointsRecord,
      isVisible: true,
      showKeypoints: false,
      color: this.getAnnotationColor(),
      compoundPath: null,
      compoundPathRecord: compoundPathRecord,
      keypoints: null,
      metadata: [],
      name: "",
      uuid: "",
      pervious: [],
      count: 0,
      currentKeypoint: null,
      keypoint: {
        tag: [],
        visibility: 0,
        next: {
          label: -1,
          visibility: 2
        }
      },
      sessions: [],
      session: {
        start: Date.now(),
        tools: [],
        milliseconds: 0
      },
      tagRecomputeCounter: 0,
      visibilityOptions: VisibilityOptions,
    };
  },
  methods: {
    ...mapMutations(["addUndo"]),
    metadataString() {
      return this.$refs.metadata.metadataString();
    },
    setKeypointsVisible(newVisible) {
      this.keypointsRecord.setKeypointsVisible(newVisible);
    },
    setKeypointsColor(newColor) {
      this.keypointsRecord.setKeypointsColor(newColor);
    },
    bringKeypointsToFront() {
      this.keypointsRecord.bringKeypointsToFront();
    },
    initAnnotation() {
      this.deleteAnnotationMetaDataName();

      this.removeCompoundPath();

      let paperObjectJson = this.getAnnotationPaperObject();
      let segmentation = this.getAnnotationSegmentation();
      this.clearCavasAndCreateCompoundPath(paperObjectJson,segmentation);
    },
    deleteAnnotationMetaDataName() {
      let metaName = this.annotation.metadata.name;
      if (metaName) {
        this.name = metaName;
        delete this.annotation.metadata["name"];
      } 
    },
    removeCompoundPath() {
      this.compoundPathRecord.removeCompoundPath(this.compoundPath);
    },
    clearCavasAndCreateCompoundPath(paperObjectJson, segments) {
      this.clearAnnotationOnCanvas();
      this.createCompoundPathAndKeypoints(paperObjectJson, segments);
      this.highlightColor();
    },
    clearAnnotationOnCanvas() {
      this.removeCompoundPath();
      this.keypointsRecord.removeKeypoints();
    },
    createCompoundPathAndKeypoints(paperObjectJson, segments) {
      this.createCompoundPathAndSetup(paperObjectJson, segments);
      this.createKeypointsAndSetup(this.$parent.category.name, this.getAnnotationId());
    },
    darkColor(color, darkHSL) {
      if (this.compoundPath) {
        this.setCompoundPathFillColor(color);
      }
      if (this.getKeypoints()) {
        this.setKeypointsColor(darkHSL);
        this.bringKeypointsToFront();
      }
    },
    highlightColor() {
      this.compoundPathRecord.highlightColor(this.compoundPath, this.opacity, this.getAnnotationColor());
      this.keypointsRecord.setKeypointsColor(this.darkHSL);
    },
    createCompoundPathAndSetup(paperObjectJson, segments) {
      this.compoundPath = new CompoundPathBuilder(        
        this.displayAnnotationSettingCallback(this.getAnnotationId()), 
        this.highlightAnnotationCallback(this.index),
        paperObjectJson, 
        segments,
        this.calculateCenter()
      )
      .withAnnotationIndex(this.index)
      .withCategoryIndex(this.categoryIndex)
      .withFullySelected(this.isAnnotationSelected)
      .withOpacity(this.opacity)
      .build()
    },
    displayAnnotationSettingCallback(annotationId) {
      return () => {
          let selectMode = this.activeTool === "Select";
          if (!selectMode) return;
          this.displayAnnotationSetting(annotationId);
      };
    },
    displayAnnotationSetting(annotationId) {
      $(`#annotationSettings${annotationId}`).modal("show");
    },
    highlightAnnotationCallback(annotationIndex) {
      return () => {
        this.hightAnnotationOnCategories(annotationIndex);
      };
    },
    hightAnnotationOnCategories(annotationIndex) {
      this.$emit("click", annotationIndex);
    },
    calculateCenter() {
      return new paper.Point(this.getAnnotationWidth() / 2, this.getAnnotationHeight() / 2);
    },
    setCompoundPathAnnotationAndCategoryIndex(annotationIndex, categoryIndex) {
      this.compoundPathRecord.setCompoundPathAnnotationAndCategoryIndex(this.compoundPath, annotationIndex, categoryIndex);
    },
    setCompoundPathFullySelected(isFullySelected) {
      this.compoundPathRecord.setCompoundPathFullySelected(this.compoundPath, isFullySelected);
    },
    setCompoundPathOpacity(newOpacity) {
      this.compoundPathRecord.setCompoundPathOpacity(this.compoundPath, newOpacity);
    },
    createKeypointsAndSetup(annotationId) {
      let keypoints = this.createKeypoints(this.getCategoryName(), annotationId);
      this.keypointsRecord.setKeypoints(keypoints);
      // this.addAnnotationKeypointsToCanvas();
    },
    getCategoryName() {
      return this.$parent.category.name;
    },
    createKeypoints(categoryName, annotationId) {
      let keypoints = new Keypoints(this.keypointEdges, this.keypointLabels,
        this.keypointColors, {
          annotationId: annotationId,
          categoryName: categoryName,
        });
      keypoints.radius = this.scale * 6;
      keypoints.lineWidth = this.scale * 2;
      return keypoints;
    },
    addAnnotationKeypointsToCanvas() {
      let keypoints = this.getAnnotationKeypoints();
      if (!keypoints || keypoints.length == 0)
        return;

      for (let i = 0; i < keypoints.length; i += 3) {
        let x = keypoints[i] - this.getAnnotationWidth() / 2,
          y = keypoints[i + 1] - this.getAnnotationHeight() / 2,
          visibility = keypoints[i + 2];
        
        let isZeroKeypoint = keypoints[i] === 0 && keypoints[i + 1] === 0 && v === 0;
        if (isZeroKeypoint) continue;
        let label = i / 3 + 1;
        this.addKeypointToRecord(new paper.Point(x, y), visibility, label);
      }
    },
    addKeypointToRecord(point, visibility, label) {
      let isDuplicatePoint = this.keypointsRecord.contains(point);
      if (label == null && isDuplicatePoint) return;
      visibility = visibility || parseInt(this.keypoint.next.visibility);
      label = label || parseInt(this.keypoint.next.label);
      let keypoint = this.createSingleKeypoint(point, visibility, label);
      this.keypointsRecord.addKeypoint(keypoint)
      this.updateKeypointLabel(label);
    },
    createSingleKeypoint(point, visibility, label) {
      let keypoint = new Keypoint(point.x, point.y, {
        visibility: visibility || 0,
        indexLabel: label || -1,
        fillColor: this.keypointColors[label - 1],
        radius: this.scale * 6,
        onClick: event => {
          if (!["Select", "Keypoints"].includes(this.activeTool)) return;
          
          let keypoint = event.target.keypoint;
          // Remove if already selected
          if (keypoint == this.currentKeypoint) {
            this.currentKeypoint = null;
            return;
          }

          this.onAnnotationClick(true);
          this.onAnnotationKeypointClick(keypoint.indexLabel - 1);

          if (this.currentKeypoint) {
            let i1 = this.currentKeypoint.indexLabel;
            let i2 = keypoint.indexLabel;
            if (this.isKeypointsNotNull() && i1 > 0 && i2 > 0) {
              let edge = [i1, i2];

              if (!this.keypointsRecord.getLine(edge)) {
                this.$parent.addKeypointEdge(edge);
              } else {
                this.$parent.removeKeypointEdge(edge);
              }
            }
          }

          this.currentKeypoint = keypoint;
        },
        onDoubleClick: this.displayKeypointsSettingCallback(),
        onMouseDrag: this.moveKeypointsCallback()
      });
      return keypoint;
    },
    displayKeypointsSettingCallback() {
      return event => {
        if (!this.$parent.isCurrent) return;
        if (!["Select", "Keypoints"].includes(this.activeTool)) return;
        this.currentKeypoint = event.target.keypoint;
        let indexLabel = this.currentKeypoint.indexLabel;

        this.keypoint.tag = indexLabel == -1 ? [] : [indexLabel.toString()];
        this.keypoint.visibility = this.currentKeypoint.visibility;
        this.displayKeypointSetting(this.getAnnotationId());
      }
    },
    moveKeypointsCallback() {
      return event => {
        let originalKeypoint = event.target.keypoint;
        let currentKeypoint = event.point;
        this.moveKeypoints(currentKeypoint, originalKeypoint);
      }
    },
    displayKeypointSetting(annotationId) {
      let keypointSettingId = `#keypointSettings${annotationId}`;
      $(keypointSettingId).modal("show");
    },
    moveKeypoints(currentKeypoint, originalKeypoint) {
      if (!["Select", "Keypoints"].includes(this.activeTool)) return;
      this.keypointsRecord.moveKeypoint(currentKeypoint, originalKeypoint);
    },
    isKeypointsNotNull() {
      return this.keypointsRecord.isKeypointsNotNull();
    },
    updateKeypointLabel(label) {
      let unusedLabels = this.notUsedKeypointLabels;
      delete unusedLabels[String(label)];
      let unusedLabelKeys = Object.keys(unusedLabels);
      if (unusedLabelKeys.length > 0) {
        let nextLabel = unusedLabelKeys[0];
        for (let ul in unusedLabels) {
          if (ul > label) {
            nextLabel = ul;
            break;
          }
        }
        this.keypoint.next.label = nextLabel;
      } else {
        this.keypoint.next.label = -1;
        this.$emit('keypoints-complete');
      }
      this.tagRecomputeCounter++;
    },
    getAnnotationCreator() {
      return this.singleAnnotationRecord.getAnnotationCreator(this.annotation);
    },
    getAnnotationId() {
      return this.singleAnnotationRecord.getAnnotationId(this.annotation);
    },
    getAnnotationWidth() {
      return this.singleAnnotationRecord.getAnnotationWidth(this.annotation);
    },
    getAnnotationHeight() {
      return this.singleAnnotationRecord.getAnnotationHeight(this.annotation);
    },
    setAnnotationIsBBox(isBBox) {
      this.singleAnnotationRecord.setAnnotationIsBBox(this.annotation, isBBox);
    },
    getAnnotationIsBBox() {
      return this.singleAnnotationRecord.getAnnotationIsBBox(this.annotation);
    },
    getAnnotationPaperObject() {
      return this.singleAnnotationRecord.getAnnotationPaperObject(this.annotation);
    },
    setAnnotationPaperObject(paper_object) {
      this.singleAnnotationRecord.setAnnotationPaperObject(this.annotation, paper_object);
    },
    getAnnotation() {
      return this.annotation;
    },
    getAnnotationKeypoints() {
      return this.singleAnnotationRecord.getAnnotationKeypoints(this.annotation);
    },
    getAnnotationSegmentation() {
      return this.singleAnnotationRecord.getAnnotationSegmentation(this.annotation);
    },
    getAnnotationColor() {
      return singleAnnotationRecord.getAnnotationColor(this.annotation);
    },
    getCompoundPath() {
      if (this.isNullCompoundPath()) {
        this.clearCavasAndCreateCompoundPath();
      }
      return this.compoundPath;
    },
    deleteAnnotation() {
      axios.delete("/api/annotation/" + this.getAnnotationId()).then(() => {
        this.socketEmitDeleteEvent();

        this.delete();

        this.notifyAnnotationDeleted();
      });
    },
    socketEmitDeleteEvent() {
      this.$socket.emit("annotation", {
        action: "delete",
        annotation: this.getAnnotation()
      });
    },
    notifyAnnotationDeleted() {
      this.$emit("deleted", this.index);
    },
    delete() {
      this.$parent.category.annotations.splice(this.index, 1);
      this.clearAnnotationOnCanvas();
    },
    
    startShowKeypoints() {
      this.showKeypoints = true;
    },
    getCategoryId() {
      return this.annotation.category_id;
    },
    onAnnotationClick(showKeypoints) {

      setSelectedAnnotation(
        this.$store,
        this.getAnnotationId(),
        this.getCategoryId()
      )
      
      if (this.keypointLabels.length) {
        this.showKeypoints = showKeypoints;
      }
      if (this.isVisible) {
        this.$emit("click", this.index);
      }
    },
    onAnnotationKeypointClick(labelIndex) {
      if (this.isKeypointLabeled(labelIndex)) {
        this.keypoint.tag = [String(labelIndex+1)];
        this.currentKeypoint = this.getKeypointsLabel(this.keypoint.tag);
      }
      if (this.isVisible) {
        this.$emit("keypoint-click", labelIndex);
      }
    },
    onAnnotationKeypointSettingsClick(labelIndex) {
      this.keypoint.tag = [String(labelIndex+1)];
      let indexLabel = parseInt(String(this.keypoint.tag));
      if (this.isKeypointsNotNull() && indexLabel in this.containsKeypointsLabel()) {
        let labelled = this.getKeypointsLabel(indexLabel);
        this.currentKeypoint = labelled;
      }
      this.keypoint.visibility = this.getKeypointVisibility(labelIndex);
    },
    onDeleteKeypointClick(labelIndex) {
      let label = String(labelIndex + 1);
      if (label in this.containsKeypointsLabel()) {
        let keypointsToDelete = this.getKeypointsLabel(label);
        this.keypointsRecord.deleteKeypoint(keypointsToDelete);
      }
    },
    onMouseEnter() {
      if (this.isNullCompoundPath()) return;

      this.compoundPathSelected()
    },
    compoundPathSelected() {
      this.compoundPath.selected = true;
    },
    onMouseLeave() {
      if (this.isNullCompoundPath()) return;

      this.compoundPathUnSelected()
    },
    compoundPathUnSelected() {
      this.compoundPath.selected = false;
    },
    isNullCompoundPath() {
      return this.compoundPath == null;
    },
    cleanAndSetCompoundPath(newCompound) {
      this.removeCompoundPath();
      this.compoundPath = newCompound;
    },
    setNullCompoundPath() {
      this.compoundPath = null;
    },
    createUndoAction(actionName, compoundPath) {
      let copy = this.compoundPathRecord.copyCompoundPath(compoundPath);

      this.pervious.push(copy);

      let action = new UndoAction({
        name: "Annotation " + this.getAnnotationId(),
        action: actionName,
        func: this.undoCompound,
        args: {}
      });
      this.addUndo(action);
    },
    isEmptyCompoundPathAndKeypoints() {
      return this.compoundPath != null && this.compoundPath.isEmpty() && this.isEmptyKeypoints();
    },
    undoCompound() {
      if (this.pervious.length == 0) return;

      this.cleanAndSetCompoundPath(this.pervious.pop());
      this.setCompoundPathFullySelected(this.isAnnotationSelected);
    },
    /**
     * Unites current annotation path with anyother path.
     * @param {paper.CompoundPath} compound compound with whoch the current annotation path unite
     * @param {boolean} simplify simplify compound after unite
     * @param {undoable} undoable add an undo action.
     * @param {isBBox} isBBox mark annotation as bbox.
     */
    unite(compound, simplify = true, undoable = true, isBBox = false) {
      if (this.isNullCompoundPath()) this.clearCavasAndCreateCompoundPath();

      let originalCompoundPath = this.getCompoundPath();

      let newCompound = this.compoundPathRecord.unitCompound(compound, originalCompoundPath);
      this.cleanAndSetCompoundPath(newCompound);
      
      this.setAnnotationIsBBox(isBBox);
      
      this.keypointsRecord.bringKeypointsToFront();
      if (simplify) this.simplifyPath();

      if (undoable) this.createUndoAction("Unite", originalCompoundPath);
    },
    simplifyPath() { 
      if (this.isEmptyCompoundPathAndKeypoints()) {
          this.deleteAnnotation();
          return;
      }
      this.compoundPath.flatten(1); // domain

      if (this.compoundPath instanceof paper.Path) {
        this.compoundPath = new paper.CompoundPath(this.compoundPath);
        this.setCompoundPathAnnotationAndCategoryIndex(this.index, this.categoryIndex);
      }
      
      this.compoundPathRecord.updateCompoundPathChildren(this.compoundPath, this.simplify);

      this.setCompoundPathFullySelected(this.isAnnotationSelected);
      this.keypointsRecord.bringKeypointsToFront();
      this.emitAnnotationModified();
    },
    emitAnnotationModified() {  
      this.setAnnotationPaperObject(
        this.exportCompoundPathJson()
      );

      this.uuid = this.getUUID();
      this.$socket.emit("annotation", {
        uuid: this.uuid,
        action: "modify",
        annotation: this.getAnnotation()
      });
    },
    /**
     * Subtract current annotation path with anyother path.
     * @param {paper.CompoundPath} compound compound to subtract current annotation path with
     * @param {boolean} simplify simplify compound after subtraction
     * @param {undoable} undoable add an undo action
     */
    subtract(compound, simplify = true, undoable = true) {
      if (this.isNullCompoundPath()) this.clearCavasAndCreateCompoundPath();
      
      let newCompound = this.compoundPath.subtract(compound);
      newCompound.onDoubleClick = this.compoundPath.onDoubleClick;
      if (undoable) this.createUndoAction("Subtract", this.compoundPath);

      
      this.cleanAndSetCompoundPath(newCompound);
      this.keypointsRecord.bringKeypointsToFront();

      if (simplify) this.simplifyPath();
    },
    setCompoundPathOpacity(newOpacity) {
      this.compoundPath.opacity = newOpacity;
    },
    setCompoundPathFillColor(newFillColor) {
      this.compoundPath.fillColor = newFillColor;
    },
    setCategory(event) {
      const newCategoryName = event.target.value;
      const annotation = this.getAnnotation();
      const oldCategory = this.$parent.category;

      this.$parent.$parent.updateAnnotationCategory(
        annotation,
        oldCategory,
        newCategoryName
      );
      $(`#annotationSettings${annotation.id}`).modal("hide");
    },
    export() {
      let annotationData = {}
      this.appendMetadataTo(annotationData);
      this.appendBasicAnnotationDataTo(annotationData);
      this.appendCompoundPathTo(annotationData);
      this.appendKeypointsTo(annotationData);
      this.appendSessionsTo(annotationData);
      return annotationData;
    },
    appendMetadataTo(annotationJson) {
      let metadata = this.$refs.metadata.export();
      if (this.name.length > 0) metadata.name = this.name;
      annotationJson['metadata'] = metadata;
    },
    appendBasicAnnotationDataTo(annotationJson) {
      annotationJson['id'] = this.getAnnotationId();
      annotationJson['isbbox'] = this.getAnnotationIsBBox();
      annotationJson['color'] = this.getAnnotationColor();
    },
    appendCompoundPathTo(annotationJson) {
      if (this.isNullCompoundPath()) {
        this.clearCavasAndCreateCompoundPath();
      }
      this.simplifyPath();
      this.setCompoundPathFullySelected(false);
      let json = this.exportCompoundPathJson();
      this.setCompoundPathFullySelected(this.isAnnotationSelected);

      let paperObjectUpdated = this.getAnnotationPaperObject() !== json;
      if (paperObjectUpdated) {
        annotationJson['compoundPath'] = json;
      }
    },
    appendKeypointsTo(annotationJson) {
      if (!this.isEmptyKeypoints()) {
        annotationJson['keypoints'] = this.keypointsRecord.exportJSONKeypoints(this.keypointLabels,
          this.getAnnotationWidth(),
          this.getAnnotationHeight());
      }
    },
    appendSessionsTo(annotationJson) {
      annotationJson['sessions'] = this.sessions;
      this.sessions = [];
    },
    exportCompoundPathJson() {
      return this.compoundPath.exportJSON({
        asString: false,
        precision: 1
      })
    },
    getUUID() {
      return Math.random()
        .toString(36)
        .replace(/[^a-z]+/g, "");
    },
    getKeypointLabel(keypoint) {
      return keypoint && keypoint.keypoints.labels[keypoint.indexLabel - 1];
    },
    isKeypointSelected(tag, index) {
      return tag == (index + 1);
    },
    isKeypointLabeled(index) {
      return this.keypointsRecord.isKeypointLabeled(index);
    },
    isEmptyKeypoints() {
      return this.keypointsRecord.isEmptyKeypoints();
    },
    getKeypoints() {
      return this.keypointsRecord.getKeypoints();
    },
    getKeypointsLabel(index) {
      return this.keypointsRecord.getKeypointsLabel(index);
    },
    containsKeypointsLabel() {
      return this.keypointsRecord.containsKeypointsLabel();
    },
    setVisible(newVisible) {
      this.visible = newVisible;
    },
    getKeypointVisibility(index) {
      return this.keypointsRecord.getKeypointVisibility(index);
    },
    getKeypointBackgroundColor(index) {
      if (this.isHover && this.$parent.isHover) return "#646c82";
      let activeIndex = this.keypoint.next.label;
      if (this.activeTool === "Select") {
        activeIndex = this.keypoint.tag;
      }
      if (this.isAnnotationSelected && activeIndex == index + 1) return "rgb(30, 86, 36)";

      return "#383c4a";
    }
  },
  watch: {
    index: {
      handler(val, oldVal) {
        
        this.initAnnotation();
        $(`#keypointSettings${this.getAnnotationId()}`).on("hidden.bs.modal", () => {
          this.currentKeypoint = null;
        });
      }
    },
    activeTool(tool) {
      if (this.isAnnotationSelected) {
        this.session.tools.push(tool);
      
        if (tool === "Keypoints") {
          if (!this.showKeypoints) {
            this.startShowKeypoints();
          }
          var labelIndex = -1;
          for(let i=0; i < this.keypointLabels.length; ++i) {
            
            if (this.isKeypointLabeled(i)) {
              if (labelIndex < 0) {
                labelIndex = i;
              }
            } else {
              labelIndex = i;
              break;
            }
          }

          if (labelIndex > -1) {
            this.keypoint.tag = [String(labelIndex+1)];
            this.currentKeypoint = this.getKeypointsLabel(this.keypoint.tag);
            this.$emit("keypoint-click", labelIndex);
          }
        }
      }
    },
    opacity(opacity) {
      this.compoundPath.opacity = opacity;
    },
    color() {
      this.highlightColor();
    },
    isVisible(newVisible) {
      if (this.isNullCompoundPath()) return;

      this.compoundPath.visible = newVisible;

      this.keypointsRecord.setKeypointsVisible(newVisible);
    },

    compoundPath() {
      if (this.isNullCompoundPath()) return;

      this.compoundPath.visible = this.isVisible;
      this.highlightColor();
    },
    keypoints() {
    },
    annotation() {
      this.initAnnotation();
    },
    isAnnotationSelected(current, wasCurrent) {
      if (current) {
        // Start new session
        this.session.start = Date.now();
        this.session.tools = [this.activeTool];
      } else {
        this.currentKeypoint = null;
      }
      if (wasCurrent) {
        // Close session
        this.session.milliseconds = Date.now() - this.session.start;
        this.sessions.push(this.session);
      }

      if (this.isNullCompoundPath()) return;
      this.setCompoundPathFullySelected(this.isAnnotationSelected);
    },
    currentKeypoint(point, old) {
      if (old) old.selected = false;
      if (point) point.selected = true;
    },
    "keypoint.tag"(newVal) {
      let id = newVal.length === 0 ? -1 : newVal[0];
      if (id !== -1) {
        this.currentKeypoint = this.getKeypointsLabel(id);
      }
      this.tagRecomputeCounter++;
    },
    "keypoint.visibility"(newVal) {
      if (!this.currentKeypoint) return;
      this.currentKeypoint.visibility = newVal;
    },
    keypointEdges(newEdges) {
      this.keypointsRecord.setKeypointsColor(this.darkHSL);
      this.keypointsRecord.addAllEdges(newEdges);
    },
    scale: {
      immediate: true,
      handler(scale) {
        if (this.keypointsRecord.isNullKeypoints()) return;

        this.keypointsRecord.setKeypointsRadius(scale * 6);
        this.keypointsRecord.setKeypointsLineWidth(scale * 2);
      }
    },
  },
  computed: {
    isAnnotationNotContainsKeypoints() {
      if (this.compoundPath == null)
        return true;

      return this.compoundPath.isEmpty() && this.isEmptyKeypoints();
    },
    categories() {
      return this.$store.getters.categories;
    },
    categoryIndex() {
      return this.$parent.index;
    },
    isAnnotationSelected() {
      let isSelected = this.index === this.current;
      let isParentCategorySelected = this.$parent.isCurrent;
      if (isSelected && isParentCategorySelected) {
        if (this.isKeypointsNotNull()) this.keypointsRecord.bringKeypointsToFront();
        return true;
      }
      return false;
    },
    keypointListView() {
      let listView = [];
      for (let i=0; i < this.keypointLabels.length; ++i) {
        let visibility = this.getKeypointVisibility(i);
        let iconColor = this.getIconColor(visibility);
        listView.push({
          label: this.keypointLabels[i],
          visibility,
          iconColor,
          backgroundColor: this.getKeypointBackgroundColor(i),
        });
      }
      return listView;
    },
    getIconColor(visibility) {
        let result = 'rgb(40, 42, 49)';
        if (visibility == 1) {
          result = 'lightgray';
        } else if (visibility == 2) {
          result = this.keypointColors[i];
        }
        return result;
    },
    isHover() {
      return this.index === this.hover;
    },
    backgroundColor() {
      if (this.isHover && this.$parent.isHover) return "#646c82";

      if (this.isAnnotationSelected) return "#4b624c";

      return "inherit";
    },
    showSideMenu() {
      let search = this.search.toLowerCase();
      if (search.length === 0) return true;
      if (search === String(this.getAnnotationId())) return true;
      if (search === String(this.index + 1)) return true;
      return this.name.toLowerCase().includes(this.search);
    },
    darkHSL() {
      let color = new paper.Color(this.getAnnotationColor());
      let h = Math.round(color.hue);
      let l = Math.round(color.lightness * 50);
      let s = Math.round(color.saturation * 100);
      return "hsl(" + h + "," + s + "%," + l + "%)";
    },
    notUsedKeypointLabels() {
      this.tagRecomputeCounter;
      let tags = {};

      for (let i = 0; i < this.keypointLabels.length; i++) {
        // Include it tags if it is the current keypoint or not in use.
        let keypointIsNotBeUsed = this.isKeypointsNotNull() && !this.getKeypointsLabel(i + 1);
        if (keypointIsNotBeUsed) {
          tags[i + 1] = this.keypointLabels[i];
        }
      }

      return tags;
    }
  },
  sockets: {
    annotation(data) {
      let annotation = data.annotation;

      if (this.uuid == data.uuid) return;
      if (annotation.id != this.getAnnotationId()) return;

      if (data.action == "modify") {
        this.clearCavasAndCreateCompoundPath(
          annotation.paper_object,
          annotation.segmentation
        );
      }

      if (data.action == "delete") {
        this.delete();
      }
    }
  },
  mounted() {
    //let a = new paper.CompoundPath();
    
    this.initAnnotation();
    $(`#keypointSettings${this.getAnnotationId()}`).on("hidden.bs.modal", () => {
      this.currentKeypoint = null;
    });
  },
  beforeDestroy() {
    this.clearAnnotationOnCanvas();
  }
};
</script>

<style scoped>
.list-group-item {
  height: 22px;
  font-size: 13px;
  padding: 2px;
  background-color: #4b5162;
}

.annotation-text {
  padding: 0;
  padding-bottom: 4px;
  margin: 0;
  line-height: 1;
}

.keypoint-list {
  float: left;
  width: 100%;
  overflow: hidden;
}

.keypoint-item {
  background-color: #383c4a;
  cursor: pointer;
}

.annotation-icon {
  margin: 0;
  padding: 3px;
}
.keypoint-icon {
  margin: 0;
  padding: 3px;
  float: left;
  padding-right: 10px;
  padding-left: 6px;
}
</style>

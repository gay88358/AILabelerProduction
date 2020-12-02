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
        <i v-if="isEmpty" style="padding-left: 5px; color: lightgray"
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
import simplifyjs from "simplify-js";
import JQuery from "jquery";
import { setSelectedAnnotation } from "../../models/actionDispatcher";
import { Keypoint, Keypoints, VisibilityOptions } from "@/libs/keypoints";
import { mapMutations } from "vuex";
import UndoAction from "@/undo";
import TagsInput from "@/components/TagsInput";
import Metadata from "@/components/Metadata";

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
      isVisible: true,
      showKeypoints: false,
      color: this.getAnnotationColor(),
      compoundPath: null,
      keypoints: null,
      metadata: [],
      isEmpty: true,
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
    initAnnotation() {
      this.deleteMetaName();
      this.removeCompoundPath();
      this.clearCavasAndCreateCompoundPath(
        this.getAnnotationPaperObject(),
        this.getAnnotationSegmentation()
      );
    },
    deleteMetaName() {
      let metaName = this.annotation.metadata.name;
      if (metaName) {
        this.name = metaName;
        delete this.annotation.metadata["name"];
      } 
    },
    isKeypointsNotNull() {
      return this.keypoints != null;
    },
    getAnnotationCreator() {
      return this.annotation.creator;
    },
    getAnnotationId() {
      return this.annotation.id;
    },
    getAnnotationWidth() {
      return this.annotation.width;
    },
    getAnnotationHeight() {
      return this.annotation.height;
    },
    setAnnotationIsBBox(isBBox) {
      this.annotation.isbbox = isBBox;
    },
    getAnnotationIsBBox() {
      return this.annotation.isbbox;
    },
    getAnnotationPaperObject() {
      return this.annotation.paper_object;
    },
    setAnnotationPaperObject(paper_object) {
      this.annotation.paper_objec = paper_object;
    },
    getAnnotation() {
      return this.annotation;
    },
    getAnnotationKeypoints() {
      return this.annotation.keypoints;
    },
    getAnnotationSegmentation() {
      return this.annotation.segmentation;
    },
    getAnnotationColor() {
      return this.annotation.color;
    },
    checkJson(json) {
      // consolidate expression to simplify nested condition checking
      if (json == null || this.noCompoundPathOrMatrix(json)) {
        return null;
      }
      return json;
    },
    noCompoundPathOrMatrix(json) {
      return json.length !== 2
    },
    checkSegments(segments) {
      // consolidate expression to simplify nested condition checking
      if (segments == null || segments.length === 0)
        return null;
      return segments;
    },
    createKeypoints(categoryName) {
      this.keypoints = new Keypoints(this.keypointEdges, this.keypointLabels,
        this.keypointColors, {
          annotationId: this.getAnnotationId(),
          categoryName: categoryName,
        });
      this.keypoints.radius = this.scale * 6;
      this.keypoints.lineWidth = this.scale * 2;
    },
    addAllAnnotationKeypoints() {
      let keypoints = this.getAnnotationKeypoints();
      if (keypoints) {
        for (let i = 0; i < keypoints.length; i += 3) {
          let x = keypoints[i] - this.getAnnotationWidth() / 2,
            y = keypoints[i + 1] - this.getAnnotationHeight() / 2,
            v = keypoints[i + 2];
          if (keypoints[i] === 0 && keypoints[i + 1] === 0 && v === 0) continue;
          this.addKeypoint(new paper.Point(x, y), v, i / 3 + 1);
        }
      }
    },
    createCompoundPathAndKeypoints() {
      this.createCompoundPath();
      // keypoints
      this.createKeypoints(this.$parent.category.name);
      this.addAllAnnotationKeypoints();
    },
    createCompoundPath() {
      this.compoundPath = new paper.CompoundPath();
      this.compoundPath.onDoubleClick = () => {
        if (this.activeTool !== "Select") return;
        $(`#annotationSettings${this.getAnnotationId()}`).modal("show");
      };
      this.compoundPath.onClick = () => {
        this.$emit("click", this.index);
      };
    },
    clearCavasAndCreateCompoundPath(json, segments) {
      this.clearAnnotationOnCanvas();
      // component setup
      this.createCompoundPathAndKeypoints();
      
      this.loadJsonOrSegmentIntoCompoundPath(json, segments);
      this.updateCompoundPathData(this.index, this.categoryIndex);
      this.setCompoundPathFullySelected(this.isCurrent);
      this.setCompoundPathOpacity(this.opacity);

      this.setColor();
    },
    loadJsonOrSegmentIntoCompoundPath(json, segments) {
      // so if compoundPath contains segment, we don't need to load segments into compoundPath
      // if we don't have compound path (which means we don't have segments), then we need to load segments into compoundPath
      json = this.checkJson(json);
      segments = this.checkSegments(segments);
      if (json != null) {
        this.compoundPath.importJSON(json);
      } else if (segments != null) {
        this.loadSegmentsIntoCompoundpath(segments, this.compoundPath);
      }
    },
    setCompoundPathOpacity(newOpacity) {
      this.compoundPath.opacity = newOpacity;
    },
    loadSegmentsIntoCompoundpath(segments, compoundPath) {
        for (let i = 0; i < segments.length; i++) {
          compoundPath.addChild(
            this.calculatePath(segments[i])
          );
        }
    },
    calculatePath(segment) {
      let result = new paper.Path();
      let center = new paper.Point(this.getAnnotationWidth() / 2, this.getAnnotationHeight() / 2);
      for (let j = 0; j < segment.length; j += 2) {
        let x = segment[j];
        let y = segment[j + 1]
        let point = new paper.Point(x, y);
        result.add(point.subtract(center));
      }
      result.closePath();
      return result;
    },
    updateCompoundPathData(annotationIndex, categoryIndex) {
      this.compoundPath.data.annotationId = annotationIndex;
      this.compoundPath.data.categoryId = categoryIndex;
    },
    deleteAnnotation() {
      axios.delete("/api/annotation/" + this.getAnnotationId()).then(() => {
        this.$socket.emit("annotation", {
          action: "delete",
          annotation: this.getAnnotation()
        });
        this.delete();

        this.$emit("deleted", this.index);
      });
    },
    delete() {
      this.$parent.category.annotations.splice(this.index, 1);
      this.clearAnnotationOnCanvas();
    },
    clearAnnotationOnCanvas() {
      this.removeCompoundPath();
      this.removeKeypoints();
    },
    removeCompoundPath() {
      if (this.isNullCompoundPath()) {
        return;
      }
      this.compoundPath.remove();
    },
    removeKeypoints() {
      if (this.isKeypointsNotNull()) {
        this.keypoints.remove();
      }
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
        this.currentKeypoint = this.keypoints._labelled[this.keypoint.tag];
      }
      if (this.isVisible) {
        this.$emit("keypoint-click", labelIndex);
      }
    },
    onAnnotationKeypointSettingsClick(labelIndex) {
      this.keypoint.tag = [String(labelIndex+1)];
      let indexLabel = parseInt(String(this.keypoint.tag));
      if (this.keypoints && indexLabel in this.keypoints._labelled) {
        let labelled = this.keypoints._labelled[indexLabel];
        this.currentKeypoint = labelled;
      }
      this.keypoint.visibility = this.getKeypointVisibility(labelIndex);
    },
    onDeleteKeypointClick(labelIndex) {
      let label = String(labelIndex + 1);
      if (label in this.keypoints._labelled) {
        this.deleteKeypoint(this.keypoints._labelled[label]);
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
    getCompoundPath() {
      if (this.isNullCompoundPath()) {
        this.clearCavasAndCreateCompoundPath();
      }
      return this.compoundPath;
    },
    setCompoundPath(newCompoundPath) {
      this.compoundPath = newCompoundPath;
    },
    setNullCompoundPath() {
      this.compoundPath = null;
    },
    setCompoundPathFullySelected(isFullySelected) {
      this.compoundPath.fullySelected = isFullySelected;
    },
    createUndoAction(actionName) {
      let copy = this.getCompoundPath().clone();
      copy.fullySelected = false;
      copy.visible = false;
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
      return this.compoundPath != null && this.compoundPath.isEmpty() && this.keypoints.isEmpty();
    },
    simplifyPath() {
      if (this.isEmptyCompoundPathAndKeypoints()) {
          this.deleteAnnotation();
          return;
      }
      this.compoundPath.flatten(1);

      if (this.compoundPath instanceof paper.Path) {
        this.compoundPath = new paper.CompoundPath(this.compoundPath);
        this.updateCompoundPathData(this.index, this.categoryIndex);
      }

      let newChildren = this.calculateCompoundPathChildren();
      this.compoundPath.removeChildren();
      this.compoundPath.addChildren(newChildren);
      this.setCompoundPathFullySelected(this.isCurrent);
      this.keypoints.bringToFront();
      this.emitModify();
    },
    calculateCompoundPathChildren() {
      let newChildren = [];
      this.compoundPath.children.forEach(path => {
        let points = [];
        path.segments.forEach(seg => {
          points.push({ x: seg.point.x, y: seg.point.y });
        });
        points = simplifyjs(points, this.simplify, true);

        let newPath = new paper.Path(points);
        newPath.closePath();
        newChildren.push(newPath);
      });
      return newChildren;
    },
    undoCompound() {
      if (this.pervious.length == 0) return;
      this.removeCompoundPath();;
      this.setCompoundPath(this.pervious.pop());
      this.setCompoundPathFullySelected(this.isCurrent);
    },
    addKeypoint(point, visibility, label) {
      let isDuplicatePoint = this.keypoints.contains(point); 
      if (label == null && isDuplicatePoint) return;

      visibility = visibility || parseInt(this.keypoint.next.visibility);
      label = label || parseInt(this.keypoint.next.label);

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
            if (this.keypoints && i1 > 0 && i2 > 0) {
              let edge = [i1, i2];

              if (!this.keypoints.getLine(edge)) {
                this.$parent.addKeypointEdge(edge);
              } else {
                this.$parent.removeKeypointEdge(edge);
              }
            }
          }

          this.currentKeypoint = keypoint;
        },
        onDoubleClick: event => {
          if (!this.$parent.isCurrent) return;
          if (!["Select", "Keypoints"].includes(this.activeTool)) return;
          this.currentKeypoint = event.target.keypoint;
          let indexLabel = this.currentKeypoint.indexLabel;

          this.keypoint.tag = indexLabel == -1 ? [] : [indexLabel.toString()];
          this.keypoint.visibility = this.currentKeypoint.visibility;
          
          let id = `#keypointSettings${this.getAnnotationId()}`;
          $(id).modal("show");
        },
        onMouseDrag: event => {
          let keypoint = event.target.keypoint;
          if (!["Select", "Keypoints"].includes(this.activeTool)) return;
          this.keypoints.moveKeypoint(event.point, keypoint);
        }
      });
      this.keypoints.addKeypoint(keypoint);
      this.isEmpty = this.compoundPath.isEmpty() && this.keypoints.isEmpty();
      this.updateKeypointLabel(label);
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
    deleteKeypoint(keypoint) {
      this.keypoints.deleteKeypoint(keypoint);
    },
    /**
     * Unites current annotation path with anyother path.
     * @param {paper.CompoundPath} compound compound to unite current annotation path with
     * @param {boolean} simplify simplify compound after unite
     * @param {undoable} undoable add an undo action.
     * @param {isBBox} isBBox mark annotation as bbox.
     */
    unite(compound, simplify = true, undoable = true, isBBox = false) {
      if (this.isNullCompoundPath()) this.clearCavasAndCreateCompoundPath();

      let newCompound = this.getCompoundPath().unite(compound);
      newCompound.strokeColor = null;
      newCompound.strokeWidth = 0;
      newCompound.onDoubleClick = this.getCompoundPath().onDoubleClick;
      newCompound.onClick = this.getCompoundPath().onClick;
      this.setAnnotationIsBBox(isBBox);

      
      if (undoable) this.createUndoAction("Unite");

      this.removeCurrentCompoundPath();
      this.setCompoundPath(newCompound);
      this.keypoints.bringToFront();

      if (simplify) this.simplifyPath();
    },
    removeCurrentCompoundPath() {
      this.getCompoundPath().remove();
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
      if (undoable) this.createUndoAction("Subtract");

      this.removeCompoundPath();;
      this.setCompoundPath(newCompound);
      this.keypoints.bringToFront();

      if (simplify) this.simplifyPath();
    },
    setColor() {
      if (this.isNullCompoundPath()) return;

      if (!this.$parent.showAnnotations) {
        this.$parent.setColor();
        return;
      }

      this.compoundPath.opacity = this.opacity;
      this.compoundPath.fillColor = this.getAnnotationColor();
      this.keypoints.color = this.darkHSL;
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
      this.setCompoundPathFullySelected(this.isCurrent);
      if (this.getAnnotationPaperObject() !== json) {
        annotationJson['compoundPath'] = json;
      }
    },
    appendKeypointsTo(annotationJson) {
      if (!this.keypoints.isEmpty()) {
        annotationJson['keypoints'] = this.keypoints.exportJSON(
          this.keypointLabels,
          this.getAnnotationWidth(),
          this.getAnnotationHeight()
        );
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
    emitModify() {
      this.uuid = Math.random()
        .toString(36)
        .replace(/[^a-z]+/g, "");
      
      this.setAnnotationPaperObject(
        this.exportCompoundPathJson()
      );

      this.$socket.emit("annotation", {
        uuid: this.uuid,
        action: "modify",
        annotation: this.getAnnotation()
      });
    },
    getKeypointLabel(keypoint) {
      return keypoint && keypoint.keypoints.labels[keypoint.indexLabel - 1];
    },
    isKeypointSelected(tag, index) {
      return tag == (index + 1);
    },
    isKeypointLabeled(index) {
      return this.keypoints && !!this.keypoints._labelled[index + 1];
    },
    getKeypointVisibility(index) {
      let visibility = 0;
      if (this.keypoints && this.keypoints._labelled) {
        let labelled = this.keypoints._labelled[index + 1];
        if (labelled) {
          visibility = labelled.visibility;
        }
      }
      return visibility;
    },
    getKeypointBackgroundColor(index) {
      if (this.isHover && this.$parent.isHover) return "#646c82";
      // if (this.keypoint.tag == index + 1) return "#4b624c";
      let activeIndex = this.keypoint.next.label;
      if (this.activeTool === "Select") {
        activeIndex = this.keypoint.tag;
      }
      if (this.isCurrent && activeIndex == index + 1) return "rgb(30, 86, 36)";

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
      if (this.isCurrent) {
        this.session.tools.push(tool);
      
        if (tool === "Keypoints") {
          if (!this.showKeypoints) {
            this.startShowKeypoints();
            // this.showKeypoints = true;
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
            this.currentKeypoint = this.keypoints._labelled[this.keypoint.tag];
            this.$emit("keypoint-click", labelIndex);
          }
        }
      }
    },
    opacity(opacity) {
      this.compoundPath.opacity = opacity;
    },
    color() {
      this.setColor();
    },
    isVisible(newVisible) {
      if (this.isNullCompoundPath()) return;

      this.compoundPath.visible = newVisible;
      this.keypoints.visible = newVisible;
    },
    compoundPath() {
      if (this.isNullCompoundPath()) return;

      this.compoundPath.visible = this.isVisible;
      this.setColor();
      this.isEmpty = this.compoundPath.isEmpty() && this.keypoints.isEmpty();
    },
    keypoints() {
      this.isEmpty = this.compoundPath.isEmpty() && this.keypoints.isEmpty();
    },
    annotation() {
      this.initAnnotation();
    },
    isCurrent(current, wasCurrent) {
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
      this.setCompoundPathFullySelected(this.isCurrent);
    },
    currentKeypoint(point, old) {
      if (old) old.selected = false;
      if (point) point.selected = true;
    },
    "keypoint.tag"(newVal) {
      let id = newVal.length === 0 ? -1 : newVal[0];
      if (id !== -1) {
        this.currentKeypoint = this.keypoints._labelled[id];
      }
      this.tagRecomputeCounter++;
    },
    "keypoint.visibility"(newVal) {
      if (!this.currentKeypoint) return;
      this.currentKeypoint.visibility = newVal;
    },
    keypointEdges(newEdges) {
      this.keypoints.color = this.darkHSL;
      newEdges.forEach(e => this.keypoints.addEdge(e));
    },
    scale: {
      immediate: true,
      handler(scale) {
        if (!this.keypoints) return;

        this.keypoints.radius = scale * 6;
        this.keypoints.lineWidth = scale * 2;
      }
    },
  },
  computed: {
    categories() {
      return this.$store.getters.categories;
    },
    categoryIndex() {
      return this.$parent.index;
    },
    isCurrent() {
      if (this.index === this.current && this.$parent.isCurrent) {
        // if (this.compoundPath != null) this.compoundPath.bringToFront();
        if (this.isKeypointsNotNull()) this.keypoints.bringToFront();
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

      if (this.isCurrent) return "#4b624c";

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
        if (this.keypoints && !this.keypoints._labelled[i + 1]) {
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

<script>
import paper from "paper";
import tool from "@/mixins/toolBar/tool";

import { invertColor } from "@/libs/colors";
import { BBox } from "@/libs/bbox";
import { mapMutations } from "vuex";
import {  polygonRecord } from "./polygonRecord";
import { CompoundPathBuilder, compoundPathRecord } from '../compoundPathRecord';
import { annotationMapper } from '../annotationMapper';

export default {
  name: "BBoxTool",
  mixins: [tool],
  props: {
    scale: {
      type: Number,
      default: 1
    },
    settings: {
      type: [Object, null],
      default: null
    }
  },
  data() {
    return {
      icon: "fa-object-group",
      name: "BBox",
      scaleFactor: 3,
      cursor: "copy",
      bbox: null,
      polygon: {
        //path: null,
        //guidance: true,
        pathOptions: {
          strokeColor: "black",
          //strokeWidth: 1
        }
      },
      polygonR: polygonRecord,
      color: {
        blackOrWhite: true,
        auto: true,
        radius: 10,
        circle: null
      },
      actionTypes: Object.freeze({
        ADD_POINTS: "Added Points",
        CLOSED_POLYGON: "Closed Polygon",
        DELETE_POLYGON: "Delete Polygon"
      }),
      actionPoints: 0
    };
  },
  methods: {
    ...mapMutations(["addUndo", "removeUndos"]),
    export() {
      return {
        completeDistance: this.getCompleteDistance(),
        minDistance: this.getMinDistance(),
        blackOrWhite: this.getColorBlackOrWhite(),
        auto: this.getColorAuto(),
        radius: this.getColorRadius()
      };
    },
    setPreferences(pref) {
      let newColorBlackOrWhite = pref.blackOrWhite || this.getColorBlackOrWhite();
      this.setColorBlackOrWhite(newColorBlackOrWhite);

      let newColorAuto = pref.auto || this.getColorAuto();
      this.setColorAuto(newColorAuto);

      let newColorRadius = pref.radius || this.getColorRadius();
      this.setColorRadius(newColorRadius);
    },
    setColorBlackOrWhite(newColorBlackOrWhite) {
      this.color.blackOrWhite = newColorBlackOrWhite;
    },
    getColorBlackOrWhite() {
      return this.color.blackOrWhite;
    },
    setColorRadius(newColorRadius) {
      this.color.radius = newColorRadius;
    },
    getColorRadius() {
      return this.color.radius;
    },
    getColorAuto() {
      return this.color.auto;
    },
    setColorAuto(newColorAuto) {
      this.color.auto = newColorAuto;
    },
    /**
     * Frees current bbox
     */
    deleteBbox() {
      let noBbox = this.isNullPolygonPath();
      if (noBbox) return;

      this.removePolygon();
      this.removeColor();
    },
    isNullPolygonPath() {
      return this.getPolygonPath() == null;
    },
    getPolygonPath() {
      return this.polygonR.getPolygonPath();
    },
    getCompleteDistance() {
      return this.polygonR.getCompleteDistance();
    },
    getMinDistance() {
      return this.polygonR.getMinDistance();
    },
    polygonSegmentLength() {
      return this.polygonR.polygonSegmentLength();
    },
    setPolygonPath(newPath) {
      this.polygonR.setPolygonPath(newPath);
    },
    setPolygonPathOptionsStrokeWidth(newStrokeWidth) {
      this.polygonR.setPolygonPathOptionsStrokeWidth(newStrokeWidth);
    },
    getPolygonPathOptions() {
      return this.polygonR.getPolygonPathOptions();
    },
    removePolygon() {
      this.polygonR.removePolygonPath();
    },
    async onMouseDown(event) {   
      if (this.isNullPolygonPath() && this.$parent.checkAnnotationExist()) {
        this.$parent.createAnnotationOnCurrentCategory();
      }
      
      if (this.isNullPolygonPath()) {
        this.createBBox(event.point);
        return;
      }

      this.updateCurrentBBox(event);
      if (this.canAddBBoxToAnnotation()) {
        await this.addBBoxToAnnotation();
      }
    },
    createBBox(point) {
      this.setPolygonPath(this.createPaperPath());
      this.bbox = new BBox(point);
      this.addBBoxPointsToPolygonPath();
    },
    /**
     * Closes current polygon and unites it with current annotaiton.
     * @returns {boolean} sucessfully closes object
     */
    canAddBBoxToAnnotation() {
      return !this.isNullPolygonPath();
    },
    async addBBoxToAnnotation() {
      if (!this.canAddBBoxToAnnotation())
        throw new Error("Check can add bbox to annotation before add bbox to annotation");

      await this.addAnnotation(this.getPolygonPath());
      this.removeData();
    },
    removeData() {
      this.removePolygon();
      this.removeColor();
      this.removeUndos(this.actionTypes.ADD_POINTS);
    },
    mapAnnotationFrom(compoundPath) {
      return annotationMapper.mapAnnotationFrom(compoundPath, this.$store);
    },
    async addAnnotation(path) {  
      //let compound = this.createCompoundPath(this.createExamplePath());
      //let annotation = await this.mapAnnotationFrom(compound);
      //this.$store.dispatch('addTempAnnotation', annotation);
      this.$parent.uniteCurrentAnnotation(path, true, true, true);
    },
    createCompoundPath(path) {
      let initialCompoundPath = new CompoundPathBuilder(
        null,
        null,        
        null, 
        null,
        new paper.Point(1202 / 2, 1208 / 2)
      )
      .withAnnotationIndex(-1)
      .withCategoryIndex(-1)
      .withFullySelected(true)
      .withOpacity(true)
      .build()

      let pathItem = compoundPathRecord.unitCompound(
        new paper.CompoundPath(path), 
        initialCompoundPath
      );
      let result = new paper.CompoundPath(pathItem);
      result.fillColor = "red";
      return result;
    },
    createExamplePath() {
      // encapsulate paper path creation details,
      // isolate bbox tool from such details
      let result = this.createPaperPath();
      result.segments = [
          [-117.97236,-189.34937],
          [-117.97236,-319.93514],
          [-232.23491,-319.93514]
        ]
      result.applyMatrix = true;
      result.strokeColor = [0, 0, 0];
      result.strokeWidth = 4.89697;
      result.closed = true;
      return result;
    },
    removeColor() {
      if (this.color.circle) {
        this.color.circle.remove();
        this.color.circle = null;
      }
    },
    onMouseMove(event) {
      if (this.isNullPolygonPath() || this.polygonSegmentLength() === 0) return;
      
      this.autoStrokeColor(event.point);
      this.updateCurrentBBox(event);
    },
    autoStrokeColor(point) {
      if (this.color.circle == null) return;
      if (this.isNullPolygonPath()) return;
      if (!this.getColorAuto()) return;

      this.color.circle.position = point;
      let color = this.$parent.image.raster.getAverageColor(this.color.circle);
      if (color) {
        this.getPolygonPathOptions().strokeColor = invertColor(
          color.toCSS(true),
          this.getColorBlackOrWhite()
        );
      }
    },
    updateCurrentBBox(event) {
      this.removeLastBBox();
      this.modifyBBox(event);
    },
    removeLastBBox() {
      this.polygonR.removeAllSegments();
      // this.getPolygonPath().removeSegments();
    },
    modifyBBox(event) {
      this.setPolygonPath(this.createPaperPath());
      this.changePointsOfBBox(event);
      this.addBBoxPointsToPolygonPath();
    },
    createPaperPath() {
      return new paper.Path(this.getPolygonPathOptions());
    },
    changePointsOfBBox(event) {
      this.bbox.modifyPoint(event.point);
    },
    addBBoxPointsToPolygonPath() {
      this.bbox.addPointsTo(this.getPolygonPath());
    },
    /**
     * Undo points
     */
    undoPoints(args) {
      if (this.isNullPolygonPath()) return;

      let points = args.points;
      this.polygonR.removeSegments(points);
    },
  },
  computed: {
    isDisabled() {
      return this.$parent.current.annotation === -1;
    }
  },
  watch: {
    isActive(active) {
      if (active) {
        this.tool.activate();
        localStorage.setItem("editorTool", this.name);
      }
    },
    /**
     * Change width of stroke based on zoom of image
     */
    scale(newScale) {
      this.setPolygonPathOptionsStrokeWidth(newScale * this.scaleFactor);
      if (this.isNullPolygonPath() == false)
        this.polygonR.setPolygonPathStrokeWidth(newScale * this.scaleFactor);
    },
    "polygon.pathOptions.strokeColor"(newColor) {
      if (this.isNullPolygonPath()) return;

      this.polygonR.setPolygonPathStrokeColor(newColor);
    },
    "color.auto"(value) {
      if (value && this.getPolygonPath()) {
        this.color.circle = new paper.Path.Rectangle(
          new paper.Point(0, 0),
          new paper.Size(10, 10)
        );
      }
      if (!value && this.color.circle) {
        this.color.circle.remove();
        this.color.circle = null;
      }
    }
  },
  created() {},
  mounted() {}
};
</script>

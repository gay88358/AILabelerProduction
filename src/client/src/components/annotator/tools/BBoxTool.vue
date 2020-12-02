<script>
import paper from "paper";
import tool from "@/mixins/toolBar/tool";
import UndoAction from "@/undo";

import { invertColor } from "@/libs/colors";
import { BBox } from "@/libs/bbox";
import { mapMutations } from "vuex";

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
        path: null,
        guidance: true,
        pathOptions: {
          strokeColor: "black",
          strokeWidth: 1
        }
      },
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
        completeDistance: this.polygon.completeDistance,
        minDistance: this.polygon.minDistance,
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
      return this.polygon.path == null;
    },
    onMouseDown(event) {      
      if (this.isNullPolygonPath() && this.$parent.checkAnnotationExist()) {
        this.$parent.createAnnotationOnCurrentCategory();
      }
      
      if (this.isNullPolygonPath()) {
        this.createBBox(event.point);
        return;
      }

      this.updateCurrentBBox(event);
      if (this.canAddBBoxToAnnotation()) {
        this.addBBoxToAnnotation();
      }
    },
    createBBox(point) {
      this.polygon.path = this.createPaperPath();
      this.bbox = new BBox(point);
      this.addPointsToPolygonPath();
    },
    /**
     * Closes current polygon and unites it with current annotaiton.
     * @returns {boolean} sucessfully closes object
     */
    canAddBBoxToAnnotation() {
      return !this.isNullPolygonPath();
    },
    addBBoxToAnnotation() {
      if (!this.canAddBBoxToAnnotation())
        throw new Error("Check can add bbox to annotation before add bbox to annotation");

      this.addAnnotation(this.polygon.path);
      this.removePolygon();
      this.removeColor();
      this.removeUndos(this.actionTypes.ADD_POINTS);
    },
    addAnnotation(path) {
      this.$parent.uniteCurrentAnnotation(path, true, true, true);
    },
    removePolygon() {
      this.polygon.path.fillColor = "black";
      this.polygon.path.closePath();
      this.polygon.path.remove();
      this.polygon.path = null;
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
        this.polygon.pathOptions.strokeColor = invertColor(
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
      this.polygon.path.removeSegments();
    },
    modifyBBox(event) {
      this.polygon.path = this.createPaperPath();
      this.changePointsOfBBox(event);
      this.addPointsToPolygonPath();
    },
    createPaperPath() {
      return new paper.Path(this.polygon.pathOptions);
    },
    changePointsOfBBox(event) {
      this.bbox.modifyPoint(event.point);
    },
    addPointsToPolygonPath() {
      this.bbox.addPointsTo(this.polygon.path);
    },
    /**
     * Undo points
     */
    undoPoints(args) {
      if (this.isNullPolygonPath()) return;

      let points = args.points;
      let length = this.polygonSegmentLength();

      this.polygon.path.removeSegments(length - points, length);
    },
    polygonSegmentLength() {
      return this.polygon.path.segments.length;
    }
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
      this.polygon.pathOptions.strokeWidth = newScale * this.scaleFactor;
      if (this.polygon.path != null)
        this.polygon.path.strokeWidth = newScale * this.scaleFactor;
    },
    "polygon.pathOptions.strokeColor"(newColor) {
      if (this.isNullPolygonPath()) return;

      this.polygon.path.strokeColor = newColor;
    },
    "color.auto"(value) {
      if (value && this.polygon.path) {
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

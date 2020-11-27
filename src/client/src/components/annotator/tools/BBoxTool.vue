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
        blackOrWhite: this.color.blackOrWhite,
        auto: this.color.auto,
        radius: this.color.radius
      };
    },
    setPreferences(pref) {
      this.color.blackOrWhite = pref.blackOrWhite || this.color.blackOrWhite;
      this.color.auto = pref.auto || this.color.auto;
      this.color.radius = pref.radius || this.color.radius;
    },
    /**
     * Frees current bbox
     */
    deleteBbox() {
      if (this.isNullPolygonPath()) return;
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
      if (this.isNullPolygonPath() || this.polygonContainsNoSegments()) return;
      
      this.autoStrokeColor(event.point);
      this.updateCurrentBBox(event);
    },
    polygonContainsNoSegments() {
      return this.polygon.path.segments.length === 0;
    },
    autoStrokeColor(point) {
      if (this.color.circle == null) return;
      if (this.isNullPolygonPath()) return;
      if (!this.color.auto) return;

      this.color.circle.position = point;
      let raster = this.$parent.image.raster;
      let color = raster.getAverageColor(this.color.circle);
      if (color) {
        this.polygon.pathOptions.strokeColor = invertColor(
          color.toCSS(true),
          this.color.blackOrWhite
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
      this.bbox.getPoints().forEach(point => this.polygon.path.add(point));
    },
    /**
     * Undo points
     */
    undoPoints(args) {
      if (this.isNullPolygonPath()) return;

      let points = args.points;
      let length = this.polygon.path.segments.length;

      this.polygon.path.removeSegments(length - points, length);
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

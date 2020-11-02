export default class DefectCodeCatalog {
    constructor(defectCodeCatalogDocument) {
        this.defectCodeCatalogDocument = defectCodeCatalogDocument
    }

    getDefectCodeListBy(categoryName) {
        let result = this.defectCodeCatalogDocument.filter(
            defectCode => defectCode.category_name === categoryName
        )
        if (result.length == 0)
            return []
        return result[0].defect_code_list;
    }
}


// defectCodeCatalogDocument = [
//         {
//             "category_name": "bsob",
//             "category_id": 0,
//             "defect_code_list": [
//                 "Second Bond Normal",
//                 "Second Bond Missing Weld",
//                 "Second Bond Broken Wire",
//                 "Second Bond Missing Weld",
//                 "Second Bond Weld ACC",
//                 "Second Bond Width Rejection",
//                 "Second Bond Length Rejection",
//                 "Second Bond Weld Clearance Error",
//                 "Not Supported",
//                 "Second Bond Weld Peeling",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Second Bond Stub Bond Distance Error",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Confirm Later"
//             ]
//         },
//         {
//             "category_name": "wire",
//             "category_id": 0,
//             "defect_code_list": [
//                 "Wire Trace Normal",
//                 "Wire Trace No Wire",
//                 "Wire Trace Wire Deviation",
//                 "Wire Trace Wire Too Close",
//                 "Wire Trace Broken Wire",
//                 "Wire Trace Snake Wire",
//                 "Not Supported",
//                 "Not Supported",
//                 "Wire Trace Short Wire",
//                 "Wire Trace Wire Sway",
//                 "Wire Trace Abnormal Wire Width",
//                 "Wire Trace Abnormal Wire Length",
//                 "Not Supported",
//                 "Not Supported",
//                 "Confirm Later"
//             ]
//         },
//         {
//             "category_name": "wedge",
//             "category_id": 0,
//             "defect_code_list": [
//                 "Second Bond Normal",
//                 "Second Bond Missing Weld",
//                 "Second Bond Broken Wire",
//                 "Second Bond Missing Weld",
//                 "Second Bond Weld ACC",
//                 "Second Bond Width Rejection",
//                 "Second Bond Length Rejection",
//                 "Second Bond Weld Clearance Error",
//                 "Not Supported",
//                 "Second Bond Weld Peeling",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Second Bond Stub Bond Distance Error",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Confirm Later"
//             ]
//         },
//         {
//             "category_name": "ball",
//             "category_id": 0,
//             "defect_code_list": [
//                 "First Bond Normal",
//                 "First Bond Missing Bond",
//                 "First Bond Broken Wire",
//                 "First Bond Ball Placement",
//                 "First Bond Ball Off Pad",
//                 "First Bond Ball Distance Error",
//                 "First Bond Wire Distance Error",
//                 "First Bond Ball Quality",
//                 "First Bond Ball Undersize",
//                 "First Bond Ball Oversize",
//                 "Not Supported",
//                 "Not Supported",
//                 "First Bond Ellipse Ratio Error",
//                 "First Bond Lifted Ball",
//                 "First Bond Golf Ball",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "Not Supported",
//                 "First Bond Twisted Neck",
//                 "First Bond Wire Over Shooting",
//                 "Not Supported",
//                 "Not Supported",
//                 "Confirm Later"
//             ]
//         }
//     ]


// function expectedDefectCodeList() {
//     return [
//         "Second Bond Normal",
//         "Second Bond Missing Weld",
//         "Second Bond Broken Wire",
//         "Second Bond Missing Weld",
//         "Second Bond Weld ACC",
//         "Second Bond Width Rejection",
//         "Second Bond Length Rejection",
//         "Second Bond Weld Clearance Error",
//         "Not Supported",
//         "Second Bond Weld Peeling",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Second Bond Stub Bond Distance Error",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Not Supported",
//         "Confirm Later"
//     ]
// }

// const assert = require('assert');

// category_name = 'bsob'
// code = new DefectCodeCatalog(defectCodeCatalogDocument)
// result = code.getDefectCodeListBy(category_name)

// actual = JSON.stringify(code.getDefectCodeListBy(category_name))
// expected = JSON.stringify(expectedDefectCodeList())
// assert.strictEqual(actual, expected)




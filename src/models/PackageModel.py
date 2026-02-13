from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package,
    Image,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Input,
    Config,
    Detection,
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputDetections(Input):
    name: Literal["inputDetections"] = "inputDetections"
    value: List[Detection]
    type: str = "object"

    class Config:
        title = "Detections"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class HeatmapInputs(Inputs):
    inputImage: InputImage
    inputDetections: InputDetections


class HeatmapOutputs(Outputs):
    outputImage: OutputImage


class MovementIouThreshold(Config):
    """
    Determines how much an object must move to generate heat.
    - Low values (e.g., 0.5): Even slight movements trigger the heatmap.
    - High values (e.g., 0.9): Only significant location changes are recorded.
    """

    name: Literal["MovementIouThreshold"] = "MovementIouThreshold"
    value: float = Field(default=0.9, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.0, 1.0]"] = "[0.0, 1.0]"

    class Config:
        title = "Movement IoU Threshold"
        json_schema_extra = {
            "shortDescription": "Motion Sensitivity"
        }


class FilterIdleDetectionsEnable(Config):
    name: Literal["FilterIdleDetectionsEnable"] = "FilterIdleDetectionsEnable"
    movementIouThreshold: MovementIouThreshold
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class FilterIdleDetectionsDisable(Config):
    name: Literal["FilterIdleDetectionsDisable"] = "FilterIdleDetectionsDisable"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class FilterIdleDetections(Config):
    """
    Prevents stationary objects from creating permanent hot spots.
    When enabled, objects must be moving to contribute to the heatmap.
    """

    name: Literal["FilterIdleDetections"] = "FilterIdleDetections"
    value: Union[FilterIdleDetectionsEnable, FilterIdleDetectionsDisable]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Filter Idle Detections"
        json_schema_extra = {
            "shortDescription": "Ignore Stationary Objects"
        }


class ColorMapAutumn(Config):
    name: Literal["ColorMapAutumn"] = "ColorMapAutumn"
    value: Literal["COLORMAP_AUTUMN"] = "COLORMAP_AUTUMN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Autumn"


class ColorMapBone(Config):
    name: Literal["ColorMapBone"] = "ColorMapBone"
    value: Literal["COLORMAP_BONE"] = "COLORMAP_BONE"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Bone"


class ColorMapJet(Config):
    name: Literal["ColorMapJet"] = "ColorMapJet"
    value: Literal["COLORMAP_JET"] = "COLORMAP_JET"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Jet"


class ColorMapWinter(Config):
    name: Literal["ColorMapWinter"] = "ColorMapWinter"
    value: Literal["COLORMAP_WINTER"] = "COLORMAP_WINTER"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Winter"


class ColorMapRainbow(Config):
    name: Literal["ColorMapRainbow"] = "ColorMapRainbow"
    value: Literal["COLORMAP_RAINBOW"] = "COLORMAP_RAINBOW"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Rainbow"


class ColorMapOcean(Config):
    name: Literal["ColorMapOcean"] = "ColorMapOcean"
    value: Literal["COLORMAP_OCEAN"] = "COLORMAP_OCEAN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Ocean"


class ColorMapSummer(Config):
    name: Literal["ColorMapSummer"] = "ColorMapSummer"
    value: Literal["COLORMAP_SUMMER"] = "COLORMAP_SUMMER"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Summer"


class ColorMapSpring(Config):
    name: Literal["ColorMapSpring"] = "ColorMapSpring"
    value: Literal["COLORMAP_SPRING"] = "COLORMAP_SPRING"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Spring"


class ColorMapCool(Config):
    name: Literal["ColorMapCool"] = "ColorMapCool"
    value: Literal["COLORMAP_COOL"] = "COLORMAP_COOL"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Cool"


class ColorMapHsv(Config):
    name: Literal["ColorMapHsv"] = "ColorMapHsv"
    value: Literal["COLORMAP_HSV"] = "COLORMAP_HSV"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "HSV"


class ColorMapPink(Config):
    name: Literal["ColorMapPink"] = "ColorMapPink"
    value: Literal["COLORMAP_PINK"] = "COLORMAP_PINK"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Pink"


class ColorMapHot(Config):
    name: Literal["ColorMapHot"] = "ColorMapHot"
    value: Literal["COLORMAP_HOT"] = "COLORMAP_HOT"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Hot"


class ColorMapParula(Config):
    name: Literal["ColorMapParula"] = "ColorMapParula"
    value: Literal["COLORMAP_PARULA"] = "COLORMAP_PARULA"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Parula"


class ColorMapMagma(Config):
    name: Literal["ColorMapMagma"] = "ColorMapMagma"
    value: Literal["COLORMAP_MAGMA"] = "COLORMAP_MAGMA"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Magma"


class ColorMapInferno(Config):
    name: Literal["ColorMapInferno"] = "ColorMapInferno"
    value: Literal["COLORMAP_INFERNO"] = "COLORMAP_INFERNO"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Inferno"


class ColorMapPlasma(Config):
    name: Literal["ColorMapPlasma"] = "ColorMapPlasma"
    value: Literal["COLORMAP_PLASMA"] = "COLORMAP_PLASMA"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Plasma"


class ColorMapViridis(Config):
    name: Literal["ColorMapViridis"] = "ColorMapViridis"
    value: Literal["COLORMAP_VIRIDIS"] = "COLORMAP_VIRIDIS"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Viridis"


class ColorMapCividis(Config):
    name: Literal["ColorMapCividis"] = "ColorMapCividis"
    value: Literal["COLORMAP_CIVIDIS"] = "COLORMAP_CIVIDIS"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Cividis"


class ColorMapTwilight(Config):
    name: Literal["ColorMapTwilight"] = "ColorMapTwilight"
    value: Literal["COLORMAP_TWILIGHT"] = "COLORMAP_TWILIGHT"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Twilight"


class ColorMapTwilightShifted(Config):
    name: Literal["ColorMapTwilightShifted"] = "ColorMapTwilightShifted"
    value: Literal["COLORMAP_TWILIGHT_SHIFTED"] = "COLORMAP_TWILIGHT_SHIFTED"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Twilight Shifted"


class ColorMapTurbo(Config):
    name: Literal["ColorMapTurbo"] = "ColorMapTurbo"
    value: Literal["COLORMAP_TURBO"] = "COLORMAP_TURBO"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Turbo"


class ColorMapDeepgreen(Config):
    name: Literal["ColorMapDeepgreen"] = "ColorMapDeepgreen"
    value: Literal["COLORMAP_DEEPGREEN"] = "COLORMAP_DEEPGREEN"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Deep Green"


class ColorMap(Config):
    """
    Selects the color palette used to visualize intensity.
    - 'Jet' or 'Turbo': High contrast, good for scientific visualization.
    - 'Hot': Transitions from black to red/yellow (fire-like).
    """

    name: Literal["ColorMap"] = "ColorMap"
    value: Union[
        ColorMapJet,
        ColorMapHot,
        ColorMapCool,
        ColorMapViridis,
        ColorMapAutumn,
        ColorMapBone,
        ColorMapWinter,
        ColorMapRainbow,
        ColorMapOcean,
        ColorMapSummer,
        ColorMapSpring,
        ColorMapHsv,
        ColorMapPink,
        ColorMapParula,
        ColorMapMagma,
        ColorMapInferno,
        ColorMapPlasma,
        ColorMapCividis,
        ColorMapTwilight,
        ColorMapTwilightShifted,
        ColorMapTurbo,
        ColorMapDeepgreen,
    ]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Color Map"
        json_schema_extra = {
            "shortDescription": "Heat Visualization Palette"
        }


class RadiusCoefficient(Config):
    """
    Controls the size of the 'heat spot' generated by each object.
    - Higher values: Larger, softer spots (good for sparse crowds).
    - Lower values: Smaller, sharper spots (good for dense crowds or precise tracking).
    """

    name: Literal["RadiusCoefficient"] = "RadiusCoefficient"
    value: int = Field(ge=0, le=100, default=50)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0, 100]"] = "[0, 100]"

    class Config:
        title = "Radius Coefficient"
        json_schema_extra = {
            "shortDescription": "Spot Size (0-100)"
        }


class GaussianBlurKernelSize(Config):
    """
    Smoothes the heatmap to remove jagged edges and create a fluid appearance.
    Must be an odd number (e.g., 35, 51). Higher values create a blurrier, more abstract map.
    """

    name: Literal["GaussianBlurKernelSize"] = "GaussianBlurKernelSize"
    value: int = Field(ge=0, default=35)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Gaussian Blur Kernel Size"
        json_schema_extra = {
            "shortDescription": "Blur Intensity"
        }


class HeatmapAlpha(Config):
    """
    Controls the visibility of the original camera image.
    - 1.0: Original image is fully opaque.
    - 0.5: Original image is semi-transparent.
    - 0.0: Original image is invisible (black background).
    """

    name: Literal["HeatmapAlpha"] = "HeatmapAlpha"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.0, 1.0]"] = "[0.0, 1.0]"

    class Config:
        title = "Image Weight (Alpha)"
        json_schema_extra = {
            "shortDescription": "Background Opacity"
        }


class HeatmapBeta(Config):
    """
    Controls the visibility of the heatmap colors.
    - 1.0: Heatmap is fully opaque and vibrant.
    - 0.5: Heatmap is semi-transparent.
    - 0.0: Heatmap is invisible.
    """

    name: Literal["HeatmapBeta"] = "HeatmapBeta"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.0, 1.0]"] = "[0.0, 1.0]"

    class Config:
        title = "Heatmap Weight (Beta)"
        json_schema_extra = {
            "shortDescription": "Heatmap Opacity"
        }


class HeatmapGamma(Config):
    """
    Fine-tunes the overall brightness of the final image.
    Use positive values to brighten dark scenes, or negative values to reduce glare.
    """

    name: Literal["HeatmapGamma"] = "HeatmapGamma"
    value: float = Field(default=0.0, ge=-50.0, le=50.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-50.0, 50.0]"] = "[-50.0, 50.0]"

    class Config:
        title = "Brightness Adjustment (Gamma)"
        json_schema_extra = {
            "shortDescription": "Brightness Offset"
        }


class DecayFactor(Config):
    """
    Determines how fast old heat trails fade away.
    - 0.99: Trails persist for a long time (Historical view).
    - 0.50: Trails fade quickly (Instantaneous view).
    - 1.00: Trails never fade (Infinite accumulation).
    """

    name: Literal["DecayFactor"] = "DecayFactor"
    value: float = Field(ge=0.5, le=1.0, default=0.99)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.5, 1.0]"] = "[0.5, 1.0]"

    class Config:
        title = "Decay Factor"
        json_schema_extra = {
            "shortDescription": "Trail Fade Rate"
        }


class HeatIntensityDivisor(Config):
    """
    Regulates the sensitivity of the 'Red' (Hot) zones.
    - Higher values (e.g., 50): Requires many people/movements to turn a spot red.
    - Lower values (e.g., 5): A single person can quickly turn a spot red.
    """

    name: Literal["HeatIntensityDivisor"] = "HeatIntensityDivisor"
    value: float = Field(ge=1.0, le=50.0, default=25.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[1.0, 50.0]"] = "[1.0, 50.0]"

    class Config:
        title = "Heat Intensity Divisor"
        json_schema_extra = {
            "shortDescription": "Saturation Sensitivity"
        }


class AdvancedEnable(Config):
    name: Literal["AdvancedEnable"] = "AdvancedEnable"
    gaussianBlurKernelSize: GaussianBlurKernelSize
    heatmapAlpha: HeatmapAlpha
    heatmapBeta: HeatmapBeta
    heatmapGamma: HeatmapGamma
    value: Literal["True"] = "True"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class AdvancedDisable(Config):
    name: Literal["AdvancedDisable"] = "AdvancedDisable"
    value: Literal["False"] = "False"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class AdvancedConfigs(Config):
    """
    Unlocks fine-tuning controls for blending, blur, and brightness.
    Enable this if the default visual style needs adjustment.
    """

    name: Literal["AdvancedConfigs"] = "AdvancedConfigs"
    value: Union[AdvancedEnable, AdvancedDisable]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Advanced"
        json_schema_extra = {
            "shortDescription": "Expert Visual Settings"
        }


class HeatmapConfigs(Configs):
    filterIdleDetections: FilterIdleDetections
    colorMap: ColorMap
    radiusCoeff: RadiusCoefficient
    decayFactor: DecayFactor
    heatIntensityDivisor: HeatIntensityDivisor
    advancedConfigs: AdvancedConfigs


class HeatmapRequest(Request):
    inputs: Optional[HeatmapInputs]
    configs: HeatmapConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class HeatmapResponse(Response):
    outputs: HeatmapOutputs


class HeatmapExecutor(Config):
    name: Literal["HeatmapExecutor"] = "HeatmapExecutor"
    value: Union[HeatmapRequest, HeatmapResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Heatmap"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[HeatmapExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {"target": "value"}


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Heatmap"] = "Heatmap"
# Workflow Node Descriptions

This document was assembled from approved workflow/node description text files. It summarizes the human-readable roles of the DIS/TOMO workflow description modules without adding synthetic workflow nodes.

## Source Files

- drug identification guide.txt
- drug_disintegration_color_change.txt
- drug_disintegration_dissolution_medium.txt
- drug_disintegration_dissolution_speed_and_time.txt
- drug_disintegration_fragment_distribution_with_density.txt
- drug_disintegration_introduction.txt
- drug_disintegration_physical_state_change.txt
- drug_disintegration_shape_change.txt
- drug_disintegration_summary.txt
- drug_disintegration_surface_texture_change.txt
- drug_disintegration_volume_change.txt

## drug identification guide

{
  "drug_identification_guide": {
    "size_and_shape": {
      "description": "This section describes how the size and shape of the drug affect its disintegration and can be used to identify the drug.",
      "examples": [
        {
          "drug": "Tablet",
          "shape": "Round",
          "size": "Small",
          "description": "Small round tablets usually dissolve faster and exhibit a rapid color change."
        },
        {
          "drug": "Capsule",
          "shape": "Oval",
          "size": "Large",
          "description": "Large oval capsules tend to take longer to dissolve, and their disintegration can be slower."
        },
        {
          "drug": "Film-coated Tablet",
          "shape": "Round",
          "size": "Medium",
          "description": "Film-coated tablets dissolve more slowly due to the coating, often resulting in gradual color change in the solution."
        }
      ]
    },
    "solution_transparency": {
      "description": "This section describes how the transparency of the solution changes as the drug dissolves and how this can be used to identify the drug.",
      "examples": [
        {
          "drug": "Aspirin",
          "transparency_change": "Becomes slightly turbid",
          "description": "Aspirin typically causes the solution to become slightly turbid as it dissolves, with a faint white cloudiness."
        },
        {
          "drug": "Paracetamol",
          "transparency_change": "Clear solution",
          "description": "Paracetamol dissolves to form a clear solution, with minimal to no turbidity."
        },
        {
          "drug": "Ibuprofen",
          "transparency_change": "Becomes cloudy",
          "description": "Ibuprofen dissolution results in a cloudy solution, indicating partial solubility and slower disintegration."
        }
      ]
    }
  }
}

## drug disintegration color change

{
  "color_change": {
    "overview": "Color change is a crucial indicator of drug disintegration. It involves assessing variations in the color intensity, transparency, and spatial distribution throughout the disintegration process.",
    "aspects": {
      "transparency_and_turbidity": {
        "description": "Describe how the dissolution medium changes from being clear to becoming turbid.",
        "example": "The initially clear solution gradually turns turbid as the tablet disintegrates, with increasing opacity."
      },
      "color_intensity_changes": {
        "description": "Record how the color intensity evolves over time.",
        "example": "The solution gradually transitions from a faint hue to a deep color, intensifying as disintegration proceeds."
      },
      "spatial_distribution_of_color": {
        "description": "Identify whether color changes occur uniformly or locally within the dissolution medium.",
        "example": "Color change begins at the interface between the tablet and the medium, gradually spreading outwards to encompass the entire medium."
      },
      "time_sequence_description": {
        "description": "Include specific timestamps to indicate color transitions.",
        "example": "At 30 seconds, the solution starts turning slightly opaque; by 1 minute, the entire solution appears fully turbid."
      }
    }
  }
}

## drug disintegration dissolution medium

{
  "dissolution_medium": {
    "overview": "This dimension focuses on the characteristics of the dissolution medium, such as pH, surfactants, and viscosity, and how they affect the disintegration.",
    "aspects": {
      "chemical_composition_and_ph_influence": {
        "description": "Describe how the type of medium and pH influence the process.",
        "example": "The dissolution rate is enhanced in a phosphate buffer at pH 6.8, simulating the intestinal environment."
      },
      "surfactant_effects": {
        "description": "Explain how surfactants impact the disintegration.",
        "example": "The addition of SDS accelerates disintegration by increasing wettability and reducing surface tension."
      },
      "medium_viscosity_and_deaeration_effects": {
        "description": "Describe how physical properties like viscosity impact dissolution.",
        "example": "Higher viscosity slows down particle movement and reduces dissolution efficiency, whereas deaerated media prevent floating and ensure uniform disintegration."
      },
      "time_referenced_changes_in_medium_properties": {
        "description": "Track how medium properties affect dissolution over time.",
        "example": "Within the first minute, the dissolution rate increases significantly due to improved surface interaction provided by the surfactant."
      }
    }
  }
}

## drug disintegration dissolution speed and time

{
  "dissolution_speed_and_time": {
    "overview": "This dimension focuses on capturing the dynamic changes in the dissolution rate over time, emphasizing variations due to particle size and liquid penetration.",
    "aspects": {
      "dynamic_changes_in_dissolution_rate": {
        "description": "Describe changes in dissolution rate across different stages.",
        "example": "The dissolution rate is slow initially, increasing rapidly as the tablet breaks apart and more surface area becomes available."
      },
      "particle_formation_and_impact_on_dissolution": {
        "description": "Explain how the creation of smaller particles affects dissolution speed.",
        "example": "As larger fragments disintegrate into finer particles, the overall dissolution rate increases due to greater surface exposure."
      },
      "effect_of_liquid_penetration": {
        "description": "Describe how liquid absorption impacts dissolution speed.",
        "example": "Upon complete penetration of liquid into the core, the dissolution rate spikes, resulting in rapid fragmentation."
      },
      "time_sequence_descriptions": {
        "description": "Use timestamps to mark significant dissolution rate changes.",
        "example": "The dissolution rate peaks at 2 minutes, following rapid internal disintegration."
      }
    }
  }
}

## drug disintegration fragment distribution with density

{
  "fragment_distribution_with_density": {
    "overview": "This dimension captures the distribution and density of fragments throughout the dissolution process, detailing their size, location, and movement.",
    "aspects": {
      "fragment_generation_and_distribution": {
        "description": "Describe how fragments are generated and their spatial distribution.",
        "example": "Initially, large fragments remain near the tablet's original position, but smaller particles progressively disperse throughout the medium."
      },
      "density_variation_with_time": {
        "description": "Detail how fragment density evolves over time.",
        "example": "The majority of fragments are initially concentrated near the disintegration site, but gradually disperse, decreasing local density."
      },
      "movement_and_sedimentation_behavior": {
        "description": "Describe how fragments move and settle in the dissolution medium.",
        "example": "Larger fragments sink to the bottom, while finer particles remain suspended, creating a cloud-like turbidity."
      },
      "time_referenced_fragment_dynamics": {
        "description": "Use temporal markers to track changes in fragment distribution.",
        "example": "At 1 minute, larger fragments have settled at the bottom, while the finer particles are evenly suspended."
      }
    }
  }
}

## drug disintegration introduction

{
  "introduction": {
    "purpose": "This document provides a detailed summary and guidance for describing drug disintegration images across eight key dimensions. The goal is to enhance accuracy, clarity, and context when describing drug disintegration processes.",
    "dimensions": [
      {
        "name": "Color Change",
        "description": "Captures the variations in color intensity, transparency, and spatial distribution during drug disintegration."
      },
      {
        "name": "Shape Change",
        "description": "Tracks the overall transformation of the drug's shape from intact to fragmented."
      },
      {
        "name": "Surface Texture Change",
        "description": "Describes changes in surface texture, including roughness, cracking, and pore formation."
      },
      {
        "name": "Volume Change",
        "description": "Monitors the reduction in tablet size, correlating with its disintegration rate."
      },
      {
        "name": "Dissolution Speed and Time",
        "description": "Captures dynamic changes in dissolution rate and particle formation over time."
      },
      {
        "name": "Physical State Change",
        "description": "Documents the internal and external structure changes, including cracking, swelling, and collapse."
      },
      {
        "name": "Dissolution Medium",
        "description": "Explores the influence of medium characteristics such as pH, surfactants, and viscosity on disintegration."
      },
      {
        "name": "Fragment Distribution with Density",
        "description": "Tracks fragment distribution and density in the dissolution medium, including movement and sedimentation."
      }
    ],
    "objective": "Each dimension includes specific criteria, examples, and detailed suggestions to ensure consistent, vivid, and thorough descriptions, supporting both qualitative and quantitative analysis."
  }
}

## drug disintegration physical state change

{
  "physical_state_change": {
    "overview": "The physical state change dimension captures the transformations in the internal and external structure of the tablet, including cracking, swelling, and eventual collapse.",
    "aspects": {
      "pore_formation_and_expansion": {
        "description": "Document the progression of pore formation.",
        "example": "Pores form as liquid infiltrates, expanding and causing internal weakening."
      },
      "expansion_and_breaking_due_to_liquid_absorption": {
        "description": "Detail the impact of swelling and subsequent breaking.",
        "example": "The tablet swells significantly as it absorbs liquid, leading to increased internal tension and eventual breaking."
      },
      "particle_generation_and_movement": {
        "description": "Describe the formation and behavior of particles.",
        "example": "As the tablet disintegrates, fine particles are formed, some of which remain suspended in the medium, while others settle at the bottom."
      },
      "time_based_progression": {
        "description": "Include temporal markers to denote changes.",
        "example": "Swelling is evident within the first 45 seconds, with major fragmentation occurring by the end of the second minute."
      }
    }
  }
}

## drug disintegration shape change

{
  "shape_change": {
    "overview": "The change in the tablet's overall shape during disintegration provides critical information regarding its breakdown process, from an intact form to small fragments.",
    "aspects": {
      "transition_from_whole_to_fragmentation": {
        "description": "Describe how the drug shape changes from intact to fragmented.",
        "example": "The initially cylindrical tablet begins to break apart into smaller, irregularly shaped pieces, eventually forming multiple fragments."
      },
      "surface_structure_changes": {
        "description": "Note changes in the surface, such as the appearance of cracks or roughness.",
        "example": "The surface changes from smooth to rough as cracks and pores begin to form across the surface."
      },
      "volume_and_contour_changes": {
        "description": "Explain how the volume and contour of the tablet evolve during the disintegration.",
        "example": "The tablet's volume significantly reduces, and its contours become less defined as disintegration proceeds."
      },
      "time_based_changes": {
        "description": "Incorporate specific time markers to illustrate the transformation.",
        "example": "In the initial 30 seconds, the tablet remains largely intact, but at 1 minute, visible cracks appear, and the volume starts to decrease."
      }
    }
  }
}

## drug disintegration summary

{
  "summary": {
    "overview": "This comprehensive guide aims to systematically describe drug disintegration images, utilizing eight key dimensions to ensure every aspect of the process is detailed thoroughly.",
    "key_points": {
      "time_sequencing_importance": "Each dimension emphasizes the importance of time sequencing, dynamic transformations, and sensory-enhanced descriptions to ensure vivid, clear, and consistent analysis.",
      "support_for_qualitative_and_quantitative_analysis": "By incorporating these descriptive elements, the depiction of drug disintegration can support both qualitative and quantitative analyses for research, quality control, and educational purposes."
    },
    "conclusion": "If additional details or further exploration of specific dimensions are required, feel free to reach out. This document serves as a foundation to build highly nuanced descriptions that facilitate better understanding of the drug disintegration process."
  }
}

## drug disintegration surface texture change

{
  "surface_texture_change": {
    "overview": "Changes in the texture of the tablet surface reflect its interaction with the dissolution medium, highlighting aspects such as roughness, porosity, and structural integrity.",
    "aspects": {
      "surface_smoothness_and_roughness": {
        "description": "Document how the surface becomes rougher as disintegration progresses.",
        "example": "Initially smooth, the tablet surface gradually roughens, with tiny pores and cracks forming over time."
      },
      "formation_of_fibrous_structures": {
        "description": "Describe how fibrous or flaky structures emerge.",
        "example": "The surface fibers emerge along the cracks, creating a network of fibrous structures as the disintegration continues."
      },
      "pore_formation_and_expansion": {
        "description": "Detail the formation of pores on the surface, and how they expand.",
        "example": "Small pores form initially and continue to expand, eventually contributing to the crumbling of the tablet structure."
      },
      "peeling_and_cracking": {
        "description": "Note the progression of cracks and any peeling effect.",
        "example": "The surface begins to peel off, forming flakes, while deep cracks widen over time."
      }
    }
  }
}

## drug disintegration volume change

{
  "volume_change": {
    "overview": "Volume change involves monitoring the reduction in tablet size, which directly correlates with its rate of disintegration.",
    "aspects": {
      "overall_volume_reduction": {
        "description": "Describe the gradual reduction in the tablet's volume.",
        "example": "The height of the tablet gradually decreases, reducing its overall volume to 50% of its initial size."
      },
      "directionality_of_volume_reduction": {
        "description": "Specify if volume reduction occurs uniformly or predominantly in one direction.",
        "example": "The tablet reduces significantly in height, while its width remains largely unchanged."
      },
      "pore_expansion_and_volume_impact": {
        "description": "Explain how pore formation affects volume.",
        "example": "The tablet swells initially as pores form, but eventually collapses as the internal structure weakens."
      },
      "time_based_description": {
        "description": "Use time markers to track volume reduction.",
        "example": "By the end of the first minute, the tablet's volume had reduced noticeably, with significant collapse occurring by the third minute."
      }
    }
  }
}


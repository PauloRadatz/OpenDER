# Copyright © 2022 Electric Power Research Institute, Inc. All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met: 
# · Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# · Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# · Neither the name of the EPRI nor the names of its contributors may be used 
#   to endorse or promote products derived from this software without specific
#   prior written permission.



# -*- coding: utf-8 -*-
# @Time    : 2/12/2021 11:18 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : common_file_format.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import pathlib
import os

class DERCommonFileFormat:

    parameters_list = ['NP_NORMAL_OP_CAT', 'NP_ABNORMAL_OP_CAT', 'NP_P_MAX', 'NP_P_MAX_OVER_PF', 'NP_OVER_PF', 'NP_P_MAX_UNDER_PF', 'NP_UNDER_PF', 'NP_VA_MAX',
                       'NP_Q_MAX_INJ', 'NP_Q_MAX_ABS', 'NP_P_MAX_CHARGE', 'NP_APPARENT_POWER_CHARGE_MAX', 'NP_AC_V_NOM',
                       'AP_LIMIT_ENABLE', 'AP_LIMIT', 'ES_RANDOMIZED_DELAY', 'ES_PERMIT_SERVICE',
                       'ES_V_LOW', 'ES_V_HIGH', 'ES_F_LOW' , 'ES_F_HIGH', 'ES_DELAY', 'ES_RAMP_RATE',
                       'CONST_PF_MODE_ENABLE', 'CONST_PF_EXCITATION', 'CONST_PF', 'CONST_Q_MODE_ENABLE', 'CONST_Q', 
                       'QV_MODE_ENABLE', 'QV_VREF', 'QV_VREF_AUTO_MODE',
                       'QV_VREF_TIME', 'QV_CURVE_V2', 'QV_CURVE_Q2', 'QV_CURVE_V3', 'QV_CURVE_Q3', 'QV_CURVE_V1',
                       'QV_CURVE_Q1', 'QV_CURVE_V4', 'QV_CURVE_Q4', 'QV_OLRT', 'QP_MODE_ENABLE', 'QP_CURVE_P3_GEN',
                       'QP_CURVE_P2_GEN', 'QP_CURVE_P1_GEN','QP_CURVE_Q3_GEN', 'QP_CURVE_Q2_GEN', 'QP_CURVE_Q1_GEN', 
                       'PV_MODE_ENABLE', 'PV_CURVE_V1', 'PV_CURVE_P1', 'PV_CURVE_V2',
                       'PV_CURVE_P2', 'PV_OLRT', 
                       'OV2_TRIP_V', 'OV2_TRIP_T' , 'OV1_TRIP_V' ,'OV1_TRIP_T' , 'UV1_TRIP_V' , 'UV1_TRIP_T', 'UV2_TRIP_V',
                       'UV2_TRIP_T' , 'OF2_TRIP_F' , 'OF2_TRIP_T' , 'OF1_TRIP_F', 'OF1_TRIP_T', 'UF1_TRIP_F', 'UF1_TRIP_T',
                       'UF2_TRIP_F', 'UF2_TRIP_T', 'PF_MODE_ENABLE', 'PF_DBOF', 'PF_DBUF', 'PF_KOF', 'PF_KUF', 'PF_OLRT',
                       'NP_EFFICIENCY', 'NP_V_DC', 'P_Q_INJ_PU', 'P_Q_ABS_PU', 'Q_MAX_INJ_PU', 'Q_MAX_ABS_PU', 
                       'NP_PRIO_OUTSIDE_MIN_Q_REQ', 'NP_V_MEAS_UNBALANCE', 'NP_PHASE', 'NP_P_MIN_PU', 'AP_RT', 'CONST_PF_RT',
                       'CONST_Q_RT', 'QP_RT', 'NP_SET_EXE_TIME', 'NP_MODE_TRANSITION_TIME', 'STATUS_INIT', 'ES_RANDOMIZED_DELAY_ACTUAL', 'NP_Q_CAPABILITY_BY_P_CURVE', 'NP_Q_CAPABILITY_LOW_P']

    __slots__ = tuple(['_'+param for param in parameters_list])
 
    def __init__(self, as_file_path=pathlib.Path(os.path.dirname(__file__)).joinpath("Parameters", "AS-with std-values.csv"),
                    model_file_path=pathlib.Path(os.path.dirname(__file__)).joinpath("Parameters", "Model-parameters.csv")):

        #Read -AS DER file
        df1 = pd.read_csv(as_file_path, index_col=0)
        df1.index = df1.index.map(lambda s: s.replace("-AS",''))

        #Read Model Parameters file
        df2 = pd.read_csv(model_file_path, index_col=0)

        frames = [df1, df2]

        # Filtering dataframe with the parameters present in the parameter_list array
        df = pd.concat(frames)
        df = df.reindex(index = self.__class__.parameters_list)

        df["New Index"] = self.__class__.parameters_list
        param = df.reset_index().set_index("New Index")["VALUE"].apply(pd.to_numeric, errors="ignore")



        #Nameplate Variables with default values
        self._NP_NORMAL_OP_CAT = "CAT_A"
        self._NP_ABNORMAL_OP_CAT = "CAT_I"
        self._NP_EFFICIENCY = 1
        self._NP_P_MAX = None
        self._NP_VA_MAX = None
        self._NP_Q_MAX_INJ = None
        self._NP_Q_MAX_ABS = None
        self._NP_P_MIN_PU = 0
        self._NP_SET_EXE_TIME = 0
        self._P_Q_INJ_PU = None
        self._P_Q_ABS_PU = None
        self._Q_MAX_INJ_PU = None
        self._Q_MAX_ABS_PU = None
        self._NP_Q_CAPABILITY_BY_P_CURVE = None
        self._NP_Q_CAPABILITY_LOW_P = 'SAME'

        #DER Model Variables with default values
        self._ES_RANDOMIZED_DELAY_ACTUAL = 0
        self._AP_RT = 15
        self._CONST_PF_RT = 5
        self._CONST_Q_RT = 5
        self._QP_RT = 5
        self._PF_MODE_ENABLE = True
        self._NP_MODE_TRANSITION_TIME = 15
        self._STATUS_INIT = True
        self._NP_V_MEAS_UNBALANCE = "AVG"
        self._NP_PRIO_OUTSIDE_MIN_Q_REQ = 'REACTIVE'
        self._NP_PHASE = 'THREE'

        #Function settings with default values
        self._AP_LIMIT_ENABLE = False
        self._AP_LIMIT = 1

        self._ES_PERMIT_SERVICE = True
        self._ES_V_LOW = 0.917
        self._ES_V_HIGH = 1.05
        self._ES_F_LOW = 59.5
        self._ES_F_HIGH = 60.1
        self._ES_DELAY = 300
        self._ES_RAMP_RATE = 300
        self._ES_RANDOMIZED_DELAY = 0

        self._CONST_PF_MODE_ENABLE = False
        self._CONST_PF = 1
        self._CONST_PF_EXCITATION = "ABS"

        self._QV_MODE_ENABLE = False
        self._QV_VREF = 1
        self._QV_VREF_AUTO_MODE = False
        self._QV_VREF_TIME = 300
        self._QV_CURVE_V1 = None
        self._QV_CURVE_Q1 = None
        self._QV_CURVE_V2 = None
        self._QV_CURVE_Q2 = 0
        self._QV_CURVE_V3 = None
        self._QV_CURVE_Q3 = 0
        self._QV_CURVE_V4 = None
        self._QV_CURVE_Q4 = None
        self._QV_OLRT = 5

        self._CONST_Q_MODE_ENABLE = False
        self._CONST_Q = 0

        self._QP_CURVE_P1_GEN = None
        self._QP_CURVE_P2_GEN = 0.5
        self._QP_CURVE_Q1_GEN = 0
        self._QP_CURVE_Q2_GEN = 0
        self._QP_CURVE_P3_GEN = 1
        self._QP_CURVE_Q3_GEN = None
        self._QP_MODE_ENABLE = False

        self._PV_MODE_ENABLE = False
        self._PV_CURVE_P1 = 1
        self._PV_CURVE_V1 = 1.06
        self._PV_CURVE_P2 = None
        self._PV_CURVE_V2 = 1.1
        self._PV_OLRT = 10

        self._OV2_TRIP_V = 1.2
        self._OV2_TRIP_T = 0.16
        self._OV1_TRIP_V = 1.1
        self._OV1_TRIP_T = None
        self._UV1_TRIP_V = None
        self._UV1_TRIP_T = None
        self._UV2_TRIP_V = None
        self._UV2_TRIP_T = None
        self._OF2_TRIP_F = 62
        self._OF2_TRIP_T = 0.16
        self._OF1_TRIP_F = 61.2
        self._OF1_TRIP_T = 300
        self._UF1_TRIP_F = 58.5
        self._UF1_TRIP_T = 300
        self._UF2_TRIP_F = 56.5
        self._UF2_TRIP_T = 0.16

        self._PF_DBOF= 0.036
        self._PF_DBUF = 0.036
        self._PF_KOF = 0.05
        self._PF_KUF = 0.05
        self._PF_OLRT = 5


        if self.isNotNaN(param.NP_NORMAL_OP_CAT):
            self.NP_NORMAL_OP_CAT = param.NP_NORMAL_OP_CAT
        if self.isNotNaN(param.NP_ABNORMAL_OP_CAT):
            self.NP_ABNORMAL_OP_CAT = param.NP_ABNORMAL_OP_CAT
        if self.isNotNaN(param.NP_P_MAX):
            self.NP_P_MAX = param.NP_P_MAX
        if self.isNotNaN(param.NP_VA_MAX):
            self.NP_VA_MAX = param.NP_VA_MAX

        if self.isNotNaN(param.NP_P_MAX_OVER_PF):
            self.NP_P_MAX_OVER_PF = param.NP_P_MAX_OVER_PF
        if self.isNotNaN(param.NP_OVER_PF):
            self.NP_OVER_PF = param.NP_OVER_PF
        if self.isNotNaN(param.NP_P_MAX_UNDER_PF):
            self.NP_P_MAX_UNDER_PF = param.NP_P_MAX_UNDER_PF
        if self.isNotNaN(param.NP_UNDER_PF):
            self.NP_UNDER_PF = param.NP_UNDER_PF
        if self.isNotNaN(param.NP_VA_MAX):
            self.NP_VA_MAX = param.NP_VA_MAX
        if self.isNotNaN(param.NP_Q_MAX_INJ):
            self.NP_Q_MAX_INJ = param.NP_Q_MAX_INJ
        if self.isNotNaN(param.NP_Q_MAX_ABS):
            self.NP_Q_MAX_ABS = param.NP_Q_MAX_ABS
        if self.isNotNaN(param.NP_P_MAX_CHARGE):
            self.NP_P_MAX_CHARGE = param.NP_P_MAX_CHARGE
        if self.isNotNaN(param.NP_APPARENT_POWER_CHARGE_MAX):
            self.NP_APPARENT_POWER_CHARGE_MAX = param.NP_APPARENT_POWER_CHARGE_MAX
        if self.isNotNaN(param.NP_AC_V_NOM):
            self.NP_AC_V_NOM = param.NP_AC_V_NOM

        if self.isNotNaN(param.P_Q_ABS_PU):
            self.P_Q_ABS_PU = param.P_Q_ABS_PU
        if self.isNotNaN(param.P_Q_INJ_PU):
            self.P_Q_INJ_PU = param.P_Q_INJ_PU
        if self.isNotNaN(param.Q_MAX_ABS_PU):
            self.Q_MAX_ABS_PU = param.Q_MAX_ABS_PU
        if self.isNotNaN(param.Q_MAX_INJ_PU):
            self.Q_MAX_INJ_PU = param.Q_MAX_INJ_PU

        if self.isNotNaN(param.NP_EFFICIENCY):
            self.NP_EFFICIENCY = param.NP_EFFICIENCY

        if self.isNotNaN(param.NP_V_DC):
            self.NP_V_DC = param.NP_V_DC

        if self.isNotNaN(param.NP_PRIO_OUTSIDE_MIN_Q_REQ):
            self.NP_PRIO_OUTSIDE_MIN_Q_REQ = param.NP_PRIO_OUTSIDE_MIN_Q_REQ

        if self.isNotNaN(param.NP_V_MEAS_UNBALANCE):
            self.NP_V_MEAS_UNBALANCE = param.NP_V_MEAS_UNBALANCE

        if self.isNotNaN(param.NP_PHASE):
            self.NP_PHASE = param.NP_PHASE

        if self.isNotNaN(param.NP_P_MIN_PU):
            self.NP_P_MIN_PU = param.NP_P_MIN_PU

        if self.isNotNaN(param.ES_RANDOMIZED_DELAY_ACTUAL):
            self.ES_RANDOMIZED_DELAY_ACTUAL = param.ES_RANDOMIZED_DELAY_ACTUAL

        if self.isNotNaN(param.AP_RT):
            self.AP_RT = param.AP_RT

        if self.isNotNaN(param.CONST_PF_RT):
            self.CONST_PF_RT = param.CONST_PF_RT

        if self.isNotNaN(param.CONST_Q_RT):
            self.CONST_Q_RT = param.CONST_Q_RT

        if self.isNotNaN(param.QP_RT):
            self.QP_RT = param.QP_RT

        if self.isNotNaN(param.PF_MODE_ENABLE):
            self.PF_MODE_ENABLE = param.PF_MODE_ENABLE

        if self.isNotNaN(param.NP_SET_EXE_TIME):
            self.NP_SET_EXE_TIME = param.NP_SET_EXE_TIME

        if self.isNotNaN(param.NP_MODE_TRANSITION_TIME):
            self.NP_MODE_TRANSITION_TIME = param.NP_MODE_TRANSITION_TIME

        if self.isNotNaN(param.STATUS_INIT):
            self.STATUS_INIT = param.STATUS_INIT



        if self.isNotNaN(param.AP_LIMIT_ENABLE):
            self.AP_LIMIT_ENABLE = param.AP_LIMIT_ENABLE
        if self.isNotNaN(param.AP_LIMIT):
            self.AP_LIMIT = param.AP_LIMIT

        if self.isNotNaN(param.ES_PERMIT_SERVICE):
            self.ES_PERMIT_SERVICE = param.ES_PERMIT_SERVICE
        if self.isNotNaN(param.ES_V_LOW):
            self.ES_V_LOW = param.ES_V_LOW
        if self.isNotNaN(param.ES_V_HIGH):
            self.ES_V_HIGH= param.ES_V_HIGH

        if self.isNotNaN(param.ES_F_LOW):
            self.ES_F_LOW = param.ES_F_LOW
        if self.isNotNaN(param.ES_F_HIGH):
            self.ES_F_HIGH = param.ES_F_HIGH
        if self.isNotNaN(param.ES_DELAY):
            self.ES_DELAY = param.ES_DELAY
        if self.isNotNaN(param.ES_RAMP_RATE):
            self.ES_RAMP_RATE = param.ES_RAMP_RATE
        if self.isNotNaN(param.ES_RANDOMIZED_DELAY):
            self.ES_RANDOMIZED_DELAY = param.ES_RANDOMIZED_DELAY

        if self.isNotNaN(param.CONST_PF_MODE_ENABLE):
            self.CONST_PF_MODE_ENABLE = param.CONST_PF_MODE_ENABLE
        if self.isNotNaN(param.CONST_PF_EXCITATION):
            self.CONST_PF_EXCITATION = param.CONST_PF_EXCITATION
        if self.isNotNaN(param.CONST_PF):
            self.CONST_PF = param.CONST_PF

        if(self.NP_NORMAL_OP_CAT == "CAT_A"):
            self.QV_CURVE_V1 = 0.9
            self.QV_CURVE_Q1 = 0.25
            self.QV_CURVE_V2 = 1
            self.QV_CURVE_V3 = 1
            self.QV_CURVE_V4 = 1.1
            self.QV_CURVE_Q4 = -0.25
            self.QV_OLRT = 10
            self.QP_CURVE_Q3_GEN = -0.25
        else:
            self.QV_CURVE_V1 = 0.92
            self.QV_CURVE_Q1 = 0.44
            self.QV_CURVE_V2 = 0.98
            self.QV_CURVE_V3 = 1.02
            self.QV_CURVE_V4 = 1.08
            self.QV_CURVE_Q4 = -0.44
            self.QV_OLRT = 5
            self.QP_CURVE_Q3_GEN = -0.44

        if self.isNotNaN(param.QV_MODE_ENABLE):
            self.QV_MODE_ENABLE = param.QV_MODE_ENABLE
        if self.isNotNaN(param.QV_VREF):
            self.QV_VREF = param.QV_VREF
        if self.isNotNaN(param.QV_VREF_TIME):
            self.QV_VREF_TIME = param.QV_VREF_TIME
        if self.isNotNaN(param.QV_VREF_AUTO_MODE):
            self.QV_VREF_AUTO_MODE = param.QV_VREF_AUTO_MODE

        if self.isNotNaN(param.QV_CURVE_V1):
            self.QV_CURVE_V1 = param.QV_CURVE_V1
        if self.isNotNaN(param.QV_CURVE_V2):
            self.QV_CURVE_V2 = param.QV_CURVE_V2
        if self.isNotNaN(param.QV_CURVE_V3):
            self.QV_CURVE_V3 = param.QV_CURVE_V3
        if self.isNotNaN(param.QV_CURVE_V4):
            self.QV_CURVE_V4 = param.QV_CURVE_V4

        if self.isNotNaN(param.QV_CURVE_Q1):
            self.QV_CURVE_Q1 = param.QV_CURVE_Q1
        if self.isNotNaN(param.QV_CURVE_Q2):
            self.QV_CURVE_Q2 = param.QV_CURVE_Q2
        if self.isNotNaN(param.QV_CURVE_Q3):
            self.QV_CURVE_Q3 = param.QV_CURVE_Q3
        if self.isNotNaN(param.QV_CURVE_Q4):
            self.QV_CURVE_Q4 = param.QV_CURVE_Q4
        if self.isNotNaN(param.QV_OLRT):
            self.QV_OLRT= param.QV_OLRT

        if self.isNotNaN(param.CONST_Q_MODE_ENABLE):
            self.CONST_Q_MODE_ENABLE = param.CONST_Q_MODE_ENABLE
        if self.isNotNaN(param.CONST_Q):
            self.CONST_Q = param.CONST_Q

        if self.isNotNaN(param.QP_MODE_ENABLE):
            self.QP_MODE_ENABLE = param.QP_MODE_ENABLE

        if self.isNotNaN(param.QP_CURVE_P1_GEN):
            self.QP_CURVE_P1_GEN = param.QP_CURVE_P1_GEN
        else:
            if(self.NP_P_MIN_PU > 0.2):
                self.QP_CURVE_P1_GEN = self.NP_P_MIN_PU
            else:
                self.QP_CURVE_P1_GEN = 0.2

        if self.isNotNaN(param.QP_CURVE_P2_GEN):
            self.QP_CURVE_P2_GEN = param.QP_CURVE_P2_GEN
        if self.isNotNaN(param.QP_CURVE_P3_GEN):
            self.QP_CURVE_P3_GEN = param.QP_CURVE_P3_GEN

        if self.isNotNaN(param.QP_CURVE_Q3_GEN):
            self.QP_CURVE_Q3_GEN = param.QP_CURVE_Q3_GEN

        if self.isNotNaN(param.QP_CURVE_Q2_GEN):
            self.QP_CURVE_Q2_GEN = param.QP_CURVE_Q2_GEN
        if self.isNotNaN(param.QP_CURVE_Q1_GEN):
            self.QP_CURVE_Q1_GEN = param.QP_CURVE_Q1_GEN

        if self.isNotNaN(param.PV_MODE_ENABLE):
            self.PV_MODE_ENABLE = param.PV_MODE_ENABLE
        if self.isNotNaN(param.PV_CURVE_V1):
            self.PV_CURVE_V1 = param.PV_CURVE_V1
        if self.isNotNaN(param.PV_CURVE_P1):
            self.PV_CURVE_P1 = param.PV_CURVE_P1
        if self.isNotNaN(param.PV_CURVE_V2):
            self.PV_CURVE_V2 = param.PV_CURVE_V2
        if self.isNotNaN(param.PV_CURVE_P2):
                self.PV_CURVE_P2 = param.PV_CURVE_P2
        else:
            if(self.NP_P_MIN_PU > 0.2):
                self.PV_CURVE_P2 = 0.2
            else:
                self.PV_CURVE_P2 = self.NP_P_MIN_PU

        if self.isNotNaN(param.PV_OLRT):
            self.PV_OLRT = param.PV_OLRT

        if(self.NP_ABNORMAL_OP_CAT == "CAT_I"):
                self.OV1_TRIP_T = 2
                self.UV1_TRIP_V = 0.7
                self.UV1_TRIP_T = 2
                self.UV2_TRIP_V = 0.45
                self.UV2_TRIP_T = 0.16

        elif(self.NP_ABNORMAL_OP_CAT == "CAT_II"):
                self.OV1_TRIP_T = 2
                self.UV1_TRIP_V = 0.7
                self.UV1_TRIP_T = 10
                self.UV2_TRIP_V = 0.45
                self.UV2_TRIP_T = 0.16
        else:
                self.OV1_TRIP_T = 13
                self.UV1_TRIP_V = 0.88
                self.UV1_TRIP_T = 21
                self.UV2_TRIP_V = 0.5
                self.UV2_TRIP_T = 2

        if self.isNotNaN(param.OV2_TRIP_V):
            self.OV2_TRIP_V = param.OV2_TRIP_V
        if self.isNotNaN(param.OV2_TRIP_T):
            self.OV2_TRIP_T = param.OV2_TRIP_T
        if self.isNotNaN(param.OV1_TRIP_V):
            self.OV1_TRIP_V = param.OV1_TRIP_V
        if self.isNotNaN(param.OF2_TRIP_F):
            self.OF2_TRIP_F = param.OF2_TRIP_F
        if self.isNotNaN(param.OF1_TRIP_F):
            self.OF1_TRIP_F = param.OF1_TRIP_F
        if self.isNotNaN(param.OF1_TRIP_T):
            self.OF1_TRIP_T = param.OF1_TRIP_T
        if self.isNotNaN(param.OF2_TRIP_T):
            self.OF2_TRIP_T = param.OF2_TRIP_T
        if self.isNotNaN(param.UF1_TRIP_F):
            self.UF1_TRIP_F = param.UF1_TRIP_F
        if self.isNotNaN(param.UF1_TRIP_T):
            self.UF1_TRIP_T = param.UF1_TRIP_T
        if self.isNotNaN(param.UF2_TRIP_F):
            self.UF2_TRIP_F = param.UF2_TRIP_F
        if self.isNotNaN(param.UF2_TRIP_T):
            self.UF2_TRIP_T = param.UF2_TRIP_T

        if self.isNotNaN(param.OV1_TRIP_T):
            self.OV1_TRIP_T = param.OV1_TRIP_T
        if self.isNotNaN(param.UV1_TRIP_V):
            self.UV1_TRIP_V = param.UV1_TRIP_V
        if self.isNotNaN(param.UV1_TRIP_T):
            self.UV1_TRIP_T = param.UV1_TRIP_T
        if self.isNotNaN(param.UV2_TRIP_V):
            self.UV2_TRIP_V = param.UV2_TRIP_V
        if self.isNotNaN(param.UV2_TRIP_T):
            self.UV2_TRIP_T = param.UV2_TRIP_T



        if self.isNotNaN(param.PF_DBOF):
            self.PF_DBOF= param.PF_DBOF
        if self.isNotNaN(param.PF_DBUF):
            self.PF_DBUF = param.PF_DBUF
        if self.isNotNaN(param.PF_KOF):
            self.PF_KOF = param.PF_KOF
        if self.isNotNaN(param.PF_KUF):
            self.PF_KUF = param.PF_KUF
        if self.isNotNaN(param.PF_OLRT):
            self.PF_OLRT = param.PF_OLRT


    def model_inputs_validity_check(self):
        # Validity Check for Nameplate Parameters
        # Reference: Section 3.1 in Report #3002021694: IEEE 1547-2018 DER Model

        # TODO move some of the checks to setters and getters
        try:
            # Reference: Table 3-1 in Report #3002021694: IEEE 1547-2018 DER Model
            if(self.NP_P_MAX <= 0 or self.NP_P_MAX > self.NP_VA_MAX):
                raise ValueError("ValueError: DER nameplate active power rating should be greater than 0, and less "
                                 "than or equal to DER nameplate apparent power rating.")

            if(self.NP_NORMAL_OP_CAT == "CAT_A"):
                if(self.NP_Q_MAX_INJ < (self.NP_VA_MAX * 0.25) or self.NP_Q_MAX_ABS > self.NP_VA_MAX):
                    raise ValueError("ValueError: For category A DER, its nameplate reactive power absorption rating "
                                     "should be greater than 25%, and less than 100% of nameplate apparent power rating.")
            elif(self.NP_NORMAL_OP_CAT == "CAT_B"):
                if(self.NP_Q_MAX_INJ < (self.NP_VA_MAX * 0.44) or self.NP_Q_MAX_ABS > self.NP_VA_MAX):
                    raise ValueError("ValueError: For category B DER, its nameplate reactive power absorption rating "
                                     "should be greater than 44%, and less than 100% of nameplate apparent power rating.")
            else:
                raise ValueError("ValueError: Value of NP_NORMAL_OP_CAT should be either CAT_A or CAT_B")

            if(self.NP_Q_MAX_INJ < (self.NP_VA_MAX * 0.44) or self.NP_Q_MAX_INJ > self.NP_VA_MAX):
                raise ValueError("ValueError: Regardless DER’s category, its nameplate reactive power injection "
                                 "rating should be greater than 44%, and less than 100% of nameplate apparent power rating.")

            if(self.NP_OVER_PF < 0 or self.NP_OVER_PF > 1):
                raise ValueError("ValueError: By definition, power factor NP_OVER_PF cannot be greater than 1 or less than 0.")

            if(self.NP_UNDER_PF < 0 or self.NP_UNDER_PF > 1):
                raise ValueError("ValueError: By definition, power factor NP_UNDER_PF cannot be greater than 1 or less than 0.")

            if(self.NP_AC_V_NOM < 0):
                raise ValueError("ValueError: DER nameplate voltage should be greater than 0.")

            #Validity Check for DER Model Behavior Parameters
            # Reference: Table 3-2 in Report #3002021694: IEEE 1547-2018 DER Model
            if(self.NP_EFFICIENCY < 0 or self.NP_EFFICIENCY > 1):
                raise ValueError("ValueError: DER Efficiency should be greater than 0, and less than or equal to 1")

            if(self.NP_P_MIN_PU < 0 or self.NP_P_MIN_PU > 1):
                raise ValueError("ValueError: DER minimum active power should be greater or equal to 0, and less than 1")

            if(len(self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_INJ_PU'])!=len(self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_INJ_PU']))\
                or(len(self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_ABS_PU'])!=len(self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_ABS_PU'])):
                raise ValueError("ValueError: Check failed for reactive power curve NP_Q_CAPABILITY_BY_P_CURVE")

            if not self.der_q_capability_validity_check(self.NP_Q_CAPABILITY_BY_P_CURVE, self.NP_NORMAL_OP_CAT):
                raise ValueError("ValueError: DER reactive capability curve defined by NP_Q_CAPABILITY_BY_P_CURVE "
                                 "should be greater than the range defined in IEEE 1547-2018 Clause 5.2")

            if(self.AP_RT < 0 or self.AP_RT > 30):
                raise ValueError("ValueError: Active power limit function response time should be greater than or equal to 0, and smaller than or equal to 30 seconds, according to IEEE 1547-2018 Clause 4.6.2.")

            if(self.CONST_PF_RT < 0 or self.CONST_PF_RT > 10):
                raise ValueError("ValueError: Constant power factor function response time should be greater than or equal to 0, and smaller than or equal to 10 seconds, according to IEEE 1547-2018 Clause 5.3.2.")

            if(self.QP_RT < 0 or self.QP_RT > 10):
                raise ValueError("ValueError: Watt-var function response time should be greater than or equal to 0, and smaller than or equal to 10 seconds, according to IEEE 1547-2018 Clause 5.3.4.")

            if(self.CONST_Q_RT < 0 or self.CONST_Q_RT > 10):
                raise ValueError("ValueError: Constant reactive power function response time should be greater than or equal to 0, and smaller than or equal to 10 seconds, according to IEEE 1547-2018 Clause 5.3.5.")

            if(self.NP_SET_EXE_TIME < 0 or self.NP_SET_EXE_TIME > 30):
                raise ValueError("ValueError: Mode and setting change execution delay time should be greater than or equal to 0, and smaller than or equal to 30 seconds, according to IEEE 1547-2018 Clause 4.6.3.")

            if(self.NP_MODE_TRANSITION_TIME < 5 or self.NP_MODE_TRANSITION_TIME > 300):
                raise ValueError("ValueError: Time for DER to smoothly transition between reactive power support modes should be greater than or equal to 5 seconds, and smaller than or equal to 300 seconds, according to IEEE 1547-2018 Clause 4.6.3.")

            #Validity Check for DER Model Behavior Parameters
            # Reference: Table 3-3 in Report #3002021694: IEEE 1547-2018 DER Model
            if(self.AP_LIMIT < 0 or self.AP_LIMIT > 1):
                raise ValueError("ValueError: Active power limit function per unit setpoint should be greater than or equal to 0, and smaller than or equal to 1.")

            if(self.ES_V_LOW < 0.88 or self.ES_V_LOW > 0.95):
                raise ValueError("ValueError: check failed for ES_V_LOW. Minimum and maximum applicable voltage for enter service criteria should be within the ranges defined in IEEE 1547-2018 Clause 4.10.2")

            if(self.ES_V_HIGH < 1.05 or self.ES_V_HIGH > 1.06):
                raise ValueError("ValueError: check failed for ES_V_HIGH. Minimum and maximum applicable voltage for enter service criteria should be within the ranges defined in IEEE 1547-2018 Clause 4.10.2")

            if(self.ES_F_LOW < 59.0 or self.ES_F_LOW > 59.9):
                raise ValueError("ValueError: check failed for ES_F_LOW. Minimum and maximum applicable frequency for enter service criteria should be within the ranges defined in IEEE 1547-2018 Clause 4.10.2")

            if(self.ES_F_HIGH < 60.1 or self.ES_F_HIGH > 61):
                raise ValueError("ValueError: check failed for ES_F_HIGH. Minimum and maximum applicable frequency for enter service criteria should be within the ranges defined in IEEE 1547-2018 Clause 4.10.2")

            if(self.ES_DELAY < 0 or self.ES_DELAY > 600):
                raise ValueError("ValueError: check failed for ES_DELAY. Minimum intentional delay before initiating softstart should be greater than or equal to 0, and smaller than or equal to 600 s, according to IEEE 1547-2018 Clause 4.10.3")

            if(self.ES_RANDOMIZED_DELAY != 0):
                if(self.NP_VA_MAX > 500) or (self.ES_RANDOMIZED_DELAY < 0 or self.ES_RANDOMIZED_DELAY > 1000):
                    raise ValueError("ValueError: check failed for ES_RANDOMIZED_DELAY. If enabled, maximum time for enter service randomized delay should be greater than or equal to 1, and smaller than or equal to 1000 s, according to IEEE 1547-2018 Clause 4.10.3. Randomized delay is only applicable for DERs less than 500kVA")

            if(self.ES_RANDOMIZED_DELAY != 0 and self.ES_RAMP_RATE != 0):
                raise ValueError("ValueError: Enter service randomized delay and ramp are mutually exclusive. They cannot be enabled together")

            if(self.ES_RAMP_RATE != 0):
                if(self.ES_RAMP_RATE < 1 or self.ES_RAMP_RATE > 1000):
                    raise ValueError("ValueError: Enter service soft-start duration should be greater than or equal to 1 s, and smaller than or equal to 1000 s, according to IEEE 1547-2018 Clause 4.10.3")

            reactive_mode_list = [self.CONST_PF_MODE_ENABLE, self.CONST_Q_MODE_ENABLE, self.QV_MODE_ENABLE, self.QP_MODE_ENABLE]

            if sum([bool(x) for x in reactive_mode_list]) > 1:
                raise ValueError("ValueError: Only one of the four reactive power controlmodes (constant reactive power, constant power factor, volt-var, and watt-var) can be enabled at a time.")

            if(self.CONST_PF < 0 or self.CONST_PF > 1):
                raise ValueError("ValueError: Constant power factor function setpoint should be between 0 and 1. ")

            if(self.QV_VREF_TIME < 300 or self.QV_VREF_TIME > 5000):
                raise ValueError("ValueError: Vref adjustment time constant should be greater than or equal to 300, and smaller than or equal to 5000 s, according to IEEE 1547-2018 Clause 5.3.3")

            if(self.QV_VREF < 0.95 or self.QV_VREF > 1.05):
                raise ValueError("ValueError: V/Q Curve VRef Setting should be greater than or equal to 0.95, and smaller than or equal to 1.05 per unit, according to IEEE 1547-2018 Clause 5.3.3")

            if(self.QV_CURVE_V1 <  (self.QV_VREF - 0.18) or self.QV_CURVE_V1 > (self.QV_CURVE_V2 - 0.02)):
                raise ValueError("ValueError: check failed for QV_CURVE_V1. For the piecewise linear curve setting of volt-var control, the four corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.3")

            if(self.QV_CURVE_V2 <  (self.QV_VREF - 0.03) or self.QV_CURVE_V2 > self.QV_VREF):
                raise ValueError("ValueError: check failed for QV_CURVE_V2. For the piecewise linear curve setting of volt-var control, the four corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.3")

            if(self.QV_CURVE_V3 <  self.QV_VREF or self.QV_CURVE_V3 > (self.QV_VREF + 0.03)):
                raise ValueError("ValueError: check failed for QV_CURVE_V3. For the piecewise linear curve setting of volt-var control, the four corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.3")

            if(self.QV_CURVE_V4 <  (self.QV_CURVE_V3 + 0.02) or self.QV_CURVE_V3 > (self.QV_VREF + 0.18)):
                raise ValueError("ValueError: check failed for QV_CURVE_V4. For the piecewise linear curve setting of volt-var control, the four corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.3")

            if(self.QV_CURVE_Q1 <  0 or self.QV_CURVE_Q1 > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: check failed for QV_CURVE_Q1. Volt-var function reactive power setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings, and the ranges defined in IEEE 1547-2018 Clause 5.3.3.")

            if(self.QV_CURVE_Q2 <  (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.QV_CURVE_Q2 > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: check failed for QV_CURVE_Q2. Volt-var function reactive power setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings, and the ranges defined in IEEE 1547-2018 Clause 5.3.3.")

            if(self.QV_CURVE_Q3 <  (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.QV_CURVE_Q3 > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: check failed for QV_CURVE_Q3. Volt-var function reactive power setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings, and the ranges defined in IEEE 1547-2018 Clause 5.3.3.")

            if(self.QV_CURVE_Q4 < (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.QV_CURVE_Q4 > 0):
                raise ValueError("ValueError: check failed for QV_CURVE_Q4. Volt-var function reactive power setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings, and the ranges defined in IEEE 1547-2018 Clause 5.3.3.")

            if(self.QV_OLRT < 1 or self.QV_OLRT > 90):
                raise ValueError("ValueError: Volt-var function open loop response time should be within the range defined in IEEE 1547-2018 Clause 5.3.3")

            if(self.QP_CURVE_P1_GEN < self.NP_P_MIN_PU or self.QP_CURVE_P1_GEN > (self.QP_CURVE_P2_GEN - 0.1)):
                raise ValueError("ValueError: check failed for QP_CURVE_P1_GEN. For the piecewise linear curve setting of watt-var control, the corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.4")

            if(self.QP_CURVE_P2_GEN < 0.4 or self.QP_CURVE_P2_GEN > 0.8):
                raise ValueError("ValueError: check failed for QP_CURVE_P2_GEN. For the piecewise linear curve setting of watt-var control, the corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.4")

            if(self.QP_CURVE_P3_GEN < (self.QP_CURVE_P2_GEN + 0.1) or self.QP_CURVE_P3_GEN > 1):
                raise ValueError("ValueError: check failed for QP_CURVE_P3_GEN. For the piecewise linear curve setting of watt-var control, the corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.3.4")

            if(self.QP_CURVE_Q1_GEN < (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.QP_CURVE_Q1_GEN > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: check failed for QP_CURVE_Q1_GEN. Watt-var function voltage setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings.")

            if(self.QP_CURVE_Q2_GEN < (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.QP_CURVE_Q2_GEN > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: check failed for QP_CURVE_Q2_GEN. Watt-var function voltage setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings.")

            if(self.QP_CURVE_Q3_GEN < (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.QP_CURVE_Q3_GEN > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: check failed for QP_CURVE_Q3_GEN. Watt-var function voltage setpoints use DER nameplate apparent power rating as base. The setpoints should be within its nameplate reactive power injection and absorption ratings.")

            if(self.CONST_Q < (-self.NP_Q_MAX_ABS/self.NP_VA_MAX) or self.CONST_Q > (self.NP_Q_MAX_INJ/self.NP_VA_MAX)):
                raise ValueError("ValueError: Constant reactive power function setpoint uses DER nameplate apparent power rating as base. It should be within its nameplate reactive power injection and absorption ratings.")

            if(self.PV_CURVE_V1<1.05 or self.PV_CURVE_V1>1.09):
                raise ValueError("ValueError: check failed for PV_CURVE_V1. For the piecewise linear curve setting of volt-watt control, the two corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.4.2")

            if(self.PV_CURVE_V2<self.PV_CURVE_V1+0.01 or self.PV_CURVE_V1>1.1):
                raise ValueError("ValueError: check failed for PV_CURVE_V2. For the piecewise linear curve setting of volt-watt control, the two corner points should have their voltage settings monotonically increasing and within the ranges defined in IEEE 1547-2018 Clause 5.4.2")

            if(self.PV_CURVE_P1 < self.PV_CURVE_P2):
                raise ValueError("ValueError: check failed for PV_CURVE_P1. Volt-watt power settings should be within the ranges defined in IEEE 1547-2018 Clause 5.4.2")

            if(self.PV_CURVE_P2 < self.NP_P_MIN_PU or self.PV_CURVE_P2 > 1):
                raise ValueError("ValueError: check failed for PV_CURVE_P2. Volt-watt power settings should be within the ranges defined in IEEE 1547-2018 Clause 5.4.2")

            if(self.PV_OLRT < 0.5 or self.PV_OLRT > 60):
                raise ValueError("ValueError: Volt-watt function open loop response time should be within the range defined in IEEE 1547-2018 Clause 5.4.2")

            if(self.OV2_TRIP_T != 0.16):
                raise ValueError("ValueError: check failed for OV2_TRIP_T. Over- and under-voltage must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.OV1_TRIP_T < 1 or self.OV1_TRIP_T > 13):
                raise ValueError("ValueError: check failed for OV1_TRIP_T. Over- and under-voltage must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.UV1_TRIP_T < 2 or self.UV1_TRIP_T > 50):
                raise ValueError("ValueError: check failed for UV1_TRIP_T. Over- and under-voltage must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.UV2_TRIP_T < 0.16 or self.UV2_TRIP_T > 21):
                raise ValueError("ValueError: check failed for UV2_TRIP_T. Over- and under-voltage must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.OV2_TRIP_V != 1.2):
                raise ValueError("ValueError: check failed for OV2_TRIP_V. Over- and under-voltage must trip curve point voltage settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.OV1_TRIP_V < 1.1 or self.OV1_TRIP_V > 1.2):
                raise ValueError("ValueError: check failed for OV1_TRIP_V. Over- and under-voltage must trip curve point voltage settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.UV1_TRIP_V < 0 or self.UV1_TRIP_V > 0.88):
                raise ValueError("ValueError: check failed for UV1_TRIP_V. Over- and under-voltage must trip curve point voltage settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.UV2_TRIP_V < 0 or self.UV2_TRIP_V > 0.5):
                raise ValueError("ValueError: check failed for UV2_TRIP_V. Over- and under-voltage must trip curve point voltage settings should be within the ranges defined in IEEE 1547-2018 Clause 6.4.1")

            if(self.OF2_TRIP_T < 0.16 or self.OF2_TRIP_T > 1000):
                raise ValueError("ValueError: check failed for OF2_TRIP_T. Over- and under-frequency must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.OF1_TRIP_T < 180 or self.OF1_TRIP_T > 1000):
                raise ValueError("ValueError: check failed for OF1_TRIP_T. Over- and under-frequency must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.UF1_TRIP_T < 180 or self.UF1_TRIP_T > 1000):
                raise ValueError("ValueError: check failed for UF1_TRIP_T. Over- and under-frequency must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.UF2_TRIP_T < 0.16 or self.UF2_TRIP_T > 1000):
                raise ValueError("ValueError: check failed for UF2_TRIP_T. Over- and under-frequency must trip curve point time settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.OF2_TRIP_F < 61.8 or self.OF2_TRIP_F > 66):
                raise ValueError("ValueError: check failed for OF2_TRIP_F. Over- and under-frequency must trip curve point frequency settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.OF1_TRIP_F < 61 or self.OF1_TRIP_F > 66):
                raise ValueError("ValueError: check failed for OF1_TRIP_F. Over- and under-frequency must trip curve point frequency settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.UF1_TRIP_F < 50 or self.UF1_TRIP_F > 59):
                raise ValueError("ValueError: check failed for UF1_TRIP_F. Over- and under-frequency must trip curve point frequency settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.UF2_TRIP_F < 50 or self.UF2_TRIP_F > 57):
                raise ValueError("ValueError: check failed for UF2_TRIP_F. Over- and under-frequency must trip curve point frequency settings should be within the ranges defined in IEEE 1547-2018 Clause 6.5.1")

            if(self.PF_DBOF < 0.017 or self.PF_DBOF > 1):
                raise ValueError("ValueError: check failed for PF_DBOF. Over- and under-frequency deadband offset from nominal frequency settings for frequency-droop function should be within the ranges defined in IEEE 1547-2018 Clause 6.5.2.7.2")

            if(self.PF_DBUF < 0.017 or self.PF_DBUF > 1):
                raise ValueError("ValueError: check failed for PF_DBUF. Over- and under-frequency deadband offset from nominal frequency settings for frequency-droop function should be within the ranges defined in IEEE 1547-2018 Clause 6.5.2.7.2")

            if(self.PF_KOF < 0.02 or self.PF_KOF > 0.05):
                raise ValueError("ValueError: check failed for PF_KOF. Over- and under-frequency frequency-droop values should be within the ranges defined in IEEE 1547-2018 Clause 6.5.2.7.2")

            if(self.PF_KUF < 0.02 or self.PF_KUF > 10):
                raise ValueError("ValueError: check failed for PF_KUF. Over- and under-frequency frequency-droop values should be within the ranges defined in IEEE 1547-2018 Clause 6.5.2.7.2")

            if(self.PF_OLRT < 0.2 or self.PF_OLRT > 10):
                raise ValueError("ValueError: Frequency-droop function open-loop response time should be within the range defined in IEEE 1547-2018 Clause 6.5.2.7.2")

        except ValueError as err:
            print("Model Inputs Validity check failed", err)
            return False

        return True

    def _get_parameter_list(self, file_info_type):
        return [f"{item}-{file_info_type}" for item in self.__class__.parameters_list]

    def check_enabled(self, value):
        """
        Change ENABLED and DISABLED to bool True and False.

        Parameters
        ----------
        value: str, Value with ENABLED or DISABLED

        Returns
        -------
        : bool, True or False

        """
        if type(value) is bool:
            return value
        elif value == "ENABLED" or value == "ENABLE" or value == "enabled" or value == "enable":
            return True
        elif value == "DISABLED" or value == "DISABLE" or value == "disabled" or value == "disable":
            return False
        else:
            print("Issue with ENABLED and DISABLED values", value)

    def isNotNaN(self,param):
        #if param is NaN (Not a number), Python considers param != param. This function checks whether param is valid.
        return (param == param) and (param is not None)


    def initialize_NP_Q_CAPABILTY_BY_P_CURVE(self):

        if self.isNotNaN(self.P_Q_ABS_PU) and self.isNotNaN(self.P_Q_INJ_PU) \
            and self.isNotNaN(self.Q_MAX_ABS_PU) and self.isNotNaN(self.Q_MAX_INJ_PU):
            self.NP_Q_CAPABILITY_BY_P_CURVE = {
                'P_Q_ABS_PU': [float(x) for x in self.P_Q_ABS_PU.strip('][').split(',')],
                'Q_MAX_ABS_PU': [float(x) for x in self.Q_MAX_ABS_PU.strip('][').split(',')],
                'P_Q_INJ_PU': [float(x) for x in self.P_Q_INJ_PU.strip('][').split(',')],
                'Q_MAX_INJ_PU': [float(x) for x in self.Q_MAX_INJ_PU.strip('][').split(',')],
            }
            if self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_ABS_PU'][0] != 0:
                self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_ABS_PU'].insert(0,0)
                self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_ABS_PU'].insert(0,self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_ABS_PU'][0])
            if self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_INJ_PU'][0] != 0:
                self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_INJ_PU'].insert(0,0)
                self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_INJ_PU'].insert(0,self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_INJ_PU'][0])

            if self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_ABS_PU'][-1] < 1:
                self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_ABS_PU'].append(1)
                self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_ABS_PU'].append(self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_ABS_PU'][-1])
            if self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_INJ_PU'][-1] < 1:
                self.NP_Q_CAPABILITY_BY_P_CURVE['P_Q_INJ_PU'].append(1)
                self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_INJ_PU'].append(self.NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_INJ_PU'][-1])
        else:
            q_max_inj_pu = self.NP_Q_MAX_INJ / self.NP_VA_MAX
            q_max_abs_pu = self.NP_Q_MAX_ABS / self.NP_VA_MAX

            self.NP_Q_CAPABILITY_BY_P_CURVE = {
                'P_Q_INJ_PU': [0, 0.04999, 0.05, 0.2, 1],
                'P_Q_ABS_PU': [0, 0.04999, 0.05, 0.2, 1],
                'Q_MAX_INJ_PU': [0, 0, q_max_inj_pu/4, q_max_inj_pu, q_max_inj_pu],
                'Q_MAX_ABS_PU': [0, 0, q_max_abs_pu/4, q_max_abs_pu, q_max_abs_pu]
                }


    def der_q_capability_validity_check(self, NP_Q_CAPABILITY_BY_P_CURVE, NP_NORMAL_OP_CAT):
        """
        Check if the DER reactive power capability custom curve is greater than the requirement

        Variable used in this function:
        :NP_Q_CAPABILITY_BY_P_CURVE: User defined reactive power capability curve
        :NP_NORMAL_OP_CAT: DER normal operating performance category

        Internal variables:
        :p_capability_pu, q_capability_pu: DER Q capability curve in terms of P, user custom defined
        :p_requirement_pu, q_requirement_pu: Minimum Q capability in terms of P, defined by IEEE 1547-2018

        return: True: custom capability curve greater than the requirement
        """

        p_requirement_pu = [0, 0.0499999999, 0.05, 0.2, 1]
        q_requirement_pu = [0, 0, 0.11, 0.44, 0.44]
        p_capability_pu = NP_Q_CAPABILITY_BY_P_CURVE['P_Q_INJ_PU']
        q_capability_pu = NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_INJ_PU']

        for i in range(len(p_capability_pu)):
            if q_capability_pu[i] < np.interp(p_capability_pu[i],p_requirement_pu,q_requirement_pu):
                return False

        if NP_NORMAL_OP_CAT == 'CAT_A':
            p_requirement_pu = [0, 0.0499999999, 0.05, 0.2, 1]
            q_requirement_pu = [0, 0, 0.11, 0.44, 0.44]
        else:
            p_requirement_pu = [0, 0.0499999999, 0.05, 0.2, 1]
            q_requirement_pu = [0, 0, 0.0625, 0.25, 0.25]

        p_capability_pu = NP_Q_CAPABILITY_BY_P_CURVE['P_Q_ABS_PU']
        q_capability_pu = NP_Q_CAPABILITY_BY_P_CURVE['Q_MAX_ABS_PU']

        for i in range(len(p_capability_pu)):
            if q_capability_pu[i] < np.interp(p_capability_pu[i],p_requirement_pu,q_requirement_pu):
                return False

        return True





    @property
    def NP_NORMAL_OP_CAT(self):
        return self._NP_NORMAL_OP_CAT

    @NP_NORMAL_OP_CAT.setter
    def NP_NORMAL_OP_CAT(self, NP_NORMAL_OP_CAT):

        self._NP_NORMAL_OP_CAT = NP_NORMAL_OP_CAT

    @property
    def NP_ABNORMAL_OP_CAT(self):
        return self._NP_ABNORMAL_OP_CAT
    
    @NP_ABNORMAL_OP_CAT.setter
    def NP_ABNORMAL_OP_CAT(self, NP_ABNORMAL_OP_CAT):

        self._NP_ABNORMAL_OP_CAT = NP_ABNORMAL_OP_CAT
    
    @property
    def NP_P_MAX(self) -> float:
        return self._NP_P_MAX

    @NP_P_MAX.setter
    def NP_P_MAX(self, NP_P_MAX):

        self._NP_P_MAX = NP_P_MAX

    @property
    def NP_P_MAX_OVER_PF(self):
        return self._NP_P_MAX_OVER_PF

    @NP_P_MAX_OVER_PF.setter
    def NP_P_MAX_OVER_PF(self, NP_P_MAX_OVER_PF):

        self._NP_P_MAX_OVER_PF = NP_P_MAX_OVER_PF

    @property
    def NP_OVER_PF(self):
        return self._NP_OVER_PF

    @NP_OVER_PF.setter
    def NP_OVER_PF(self, NP_OVER_PF):

        self._NP_OVER_PF = NP_OVER_PF

    @property
    def NP_P_MAX_UNDER_PF(self):
        return self._NP_P_MAX_UNDER_PF

    @NP_P_MAX_UNDER_PF.setter
    def NP_P_MAX_UNDER_PF(self, NP_P_MAX_UNDER_PF):

        self._NP_P_MAX_UNDER_PF = NP_P_MAX_UNDER_PF

    @property
    def NP_UNDER_PF(self):
        return self._NP_UNDER_PF

    @NP_UNDER_PF.setter
    def NP_UNDER_PF(self, NP_UNDER_PF):

        self._NP_UNDER_PF = NP_UNDER_PF

    @property
    def NP_VA_MAX(self):
        return self._NP_VA_MAX

    @NP_VA_MAX.setter
    def NP_VA_MAX(self, NP_VA_MAX):

        self._NP_VA_MAX = NP_VA_MAX

    @property
    def NP_Q_MAX_INJ(self):
        return self._NP_Q_MAX_INJ

    @NP_Q_MAX_INJ.setter
    def NP_Q_MAX_INJ(self, NP_Q_MAX_INJ):

        self._NP_Q_MAX_INJ = NP_Q_MAX_INJ

    @property
    def NP_Q_MAX_ABS(self):
        return self._NP_Q_MAX_ABS

    @NP_Q_MAX_ABS.setter
    def NP_Q_MAX_ABS(self, NP_Q_MAX_ABS):

        self._NP_Q_MAX_ABS = NP_Q_MAX_ABS

    @property
    def NP_P_MAX_CHARGE(self):
        return self._NP_P_MAX_CHARGE

    @NP_P_MAX_CHARGE.setter
    def NP_P_MAX_CHARGE(self, NP_P_MAX_CHARGE):

        self._NP_P_MAX_CHARGE = NP_P_MAX_CHARGE

    @property
    def NP_APPARENT_POWER_CHARGE_MAX(self):
        return self._NP_APPARENT_POWER_CHARGE_MAX

    @NP_APPARENT_POWER_CHARGE_MAX.setter
    def NP_APPARENT_POWER_CHARGE_MAX(self, NP_APPARENT_POWER_CHARGE_MAX):

        self._NP_APPARENT_POWER_CHARGE_MAX = NP_APPARENT_POWER_CHARGE_MAX

    @property
    def NP_AC_V_NOM(self):
        return self._NP_AC_V_NOM

    @NP_AC_V_NOM.setter
    def NP_AC_V_NOM(self, NP_AC_V_NOM):

        self._NP_AC_V_NOM = NP_AC_V_NOM
        
    @property
    def NP_P_MIN_PU(self):
        return self._NP_P_MIN_PU

    @NP_P_MIN_PU.setter
    def NP_P_MIN_PU(self, NP_P_MIN_PU):

        self._NP_P_MIN_PU = NP_P_MIN_PU
        
    @property
    def NP_PHASE(self):
        return self._NP_PHASE
    
    @NP_PHASE.setter
    def NP_PHASE(self, NP_PHASE):

        self._NP_PHASE = NP_PHASE
    
    @property
    def NP_SET_EXE_TIME(self):
        return self._NP_SET_EXE_TIME
    
    @NP_SET_EXE_TIME.setter
    def NP_SET_EXE_TIME(self, NP_SET_EXE_TIME):

        self._NP_SET_EXE_TIME = NP_SET_EXE_TIME
        
    @property
    def NP_MODE_TRANSITION_TIME(self):
        return self._NP_MODE_TRANSITION_TIME
    
    @NP_MODE_TRANSITION_TIME.setter
    def NP_MODE_TRANSITION_TIME(self, NP_MODE_TRANSITION_TIME):

        self._NP_MODE_TRANSITION_TIME = NP_MODE_TRANSITION_TIME
        
    @property
    def NP_V_DC(self):
        return self._NP_AC_V_NOM
    
    @NP_V_DC.setter
    def NP_V_DC(self, NP_V_DC):

        self._NP_V_DC = NP_V_DC

    @property
    def ES_RANDOMIZED_DELAY_ACTUAL(self):
        return self._ES_RANDOMIZED_DELAY_ACTUAL

    @ES_RANDOMIZED_DELAY_ACTUAL.setter
    def ES_RANDOMIZED_DELAY_ACTUAL(self, ES_RANDOMIZED_DELAY_ACTUAL):

        self._ES_RANDOMIZED_DELAY_ACTUAL = ES_RANDOMIZED_DELAY_ACTUAL

    @property
    def AP_LIMIT_ENABLE(self):
        return self._AP_LIMIT_ENABLE
    
    @AP_LIMIT_ENABLE.setter
    def AP_LIMIT_ENABLE(self, AP_LIMIT_ENABLE):

        self._AP_LIMIT_ENABLE = self.check_enabled(AP_LIMIT_ENABLE)

    @property
    def AP_LIMIT(self):
        return self._AP_LIMIT
    
    @AP_LIMIT.setter
    def AP_LIMIT(self, AP_LIMIT):

        self._AP_LIMIT = AP_LIMIT
   
    @property
    def CONST_PF_RT(self):
        return self._CONST_PF_RT
    
    @CONST_PF_RT.setter
    def CONST_PF_RT(self, CONST_PF_RT):

        self._CONST_PF_RT = CONST_PF_RT
    
    @property
    def CONST_Q_RT(self):
        return self._CONST_Q_RT

    @CONST_Q_RT.setter
    def CONST_Q_RT(self, CONST_Q_RT):

        self._CONST_Q_RT = CONST_Q_RT
    
    @property
    def ES_PERMIT_SERVICE(self):
        return self._ES_PERMIT_SERVICE
    
    @ES_PERMIT_SERVICE.setter
    def ES_PERMIT_SERVICE(self, ES_PERMIT_SERVICE):

        self._ES_PERMIT_SERVICE= self.check_enabled(ES_PERMIT_SERVICE)
    
    @property
    def ES_V_LOW(self):
        return self._ES_V_LOW
    
    @ES_V_LOW.setter
    def ES_V_LOW(self, ES_V_LOW):

        self._ES_V_LOW= ES_V_LOW
        
    @property
    def ES_V_HIGH(self):
        return self._ES_V_HIGH
    
    @ES_V_HIGH.setter
    def ES_V_HIGH(self, ES_V_HIGH):

        self._ES_V_HIGH= ES_V_HIGH
        
    @property
    def ES_F_LOW(self):
        return self._ES_F_LOW
    
    @ES_F_LOW.setter
    def ES_F_LOW(self, ES_F_LOW):

        self._ES_F_LOW= ES_F_LOW
        
    @property
    def ES_F_HIGH(self):
        return self._ES_F_HIGH
    
    @ES_F_HIGH.setter
    def ES_F_HIGH(self, ES_F_HIGH):

        self._ES_F_HIGH= ES_F_HIGH
        
    @property
    def ES_DELAY(self):
        return self._ES_DELAY
    
    @ES_DELAY.setter
    def ES_DELAY(self, ES_DELAY):

        self._ES_DELAY= ES_DELAY
    
    @property
    def ES_RANDOMIZED_DELAY(self):
        return self._ES_RANDOMIZED_DELAY

    @ES_RANDOMIZED_DELAY.setter
    def ES_RANDOMIZED_DELAY(self, ES_RANDOMIZED_DELAY):

        self._ES_RANDOMIZED_DELAY= ES_RANDOMIZED_DELAY

    @property
    def ES_RAMP_RATE(self):
        return self._ES_RAMP_RATE

    @ES_RAMP_RATE.setter
    def ES_RAMP_RATE(self, ES_RAMP_RATE):

        self._ES_RAMP_RATE = ES_RAMP_RATE

    @property
    def CONST_PF_MODE_ENABLE(self):
        return self._CONST_PF_MODE_ENABLE

    @CONST_PF_MODE_ENABLE.setter
    def CONST_PF_MODE_ENABLE(self, CONST_PF_MODE_ENABLE):

        self._CONST_PF_MODE_ENABLE = self.check_enabled(CONST_PF_MODE_ENABLE)
        if self._CONST_PF_MODE_ENABLE:
            self.QV_MODE_ENABLE, self.QP_MODE_ENABLE, self.CONST_Q_MODE_ENABLE = False, False, False

    @property
    def CONST_PF_EXCITATION(self):
        return self._CONST_PF_EXCITATION

    @CONST_PF_EXCITATION.setter
    def CONST_PF_EXCITATION(self, CONST_PF_EXCITATION):

        self._CONST_PF_EXCITATION = CONST_PF_EXCITATION

    @property
    def CONST_PF(self):
        return self._CONST_PF

    @CONST_PF.setter
    def CONST_PF(self, CONST_PF):
        if CONST_PF < 0:
            raise ValueError("ValueError - CONST_PF must be positive")

        self._CONST_PF = CONST_PF

    @property
    def CONST_Q_MODE_ENABLE(self):
        return self._CONST_Q_MODE_ENABLE

    @CONST_Q_MODE_ENABLE.setter
    def CONST_Q_MODE_ENABLE(self, CONST_Q_MODE_ENABLE):

        self._CONST_Q_MODE_ENABLE = self.check_enabled(CONST_Q_MODE_ENABLE)
        if self._CONST_Q_MODE_ENABLE:
            self.QV_MODE_ENABLE, self.QP_MODE_ENABLE, self.CONST_PF_MODE_ENABLE = False, False, False

    @property
    def CONST_Q(self):
        return self._CONST_Q

    @CONST_Q.setter
    def CONST_Q(self, CONST_Q):

        self._CONST_Q = CONST_Q
    
    @property
    def P_Q_INJ_PU(self):
        return self._P_Q_INJ_PU
    
    @P_Q_INJ_PU.setter
    def P_Q_INJ_PU(self, P_Q_INJ_PU):

        self._P_Q_INJ_PU = P_Q_INJ_PU
    
    @property
    def P_Q_ABS_PU(self):
        return self._P_Q_ABS_PU
    
    @P_Q_ABS_PU.setter
    def P_Q_ABS_PU(self, P_Q_ABS_PU):

        self._P_Q_ABS_PU = P_Q_ABS_PU
        
    @property
    def Q_MAX_INJ_PU(self):
        return self._Q_MAX_INJ_PU
    
    @Q_MAX_INJ_PU.setter
    def Q_MAX_INJ_PU(self, Q_MAX_INJ_PU):

        self._Q_MAX_INJ_PU = Q_MAX_INJ_PU
    
    @property
    def Q_MAX_ABS_PU(self):
        return self._Q_MAX_ABS_PU
    
    @Q_MAX_ABS_PU.setter
    def Q_MAX_ABS_PU(self, Q_MAX_ABS_PU):

        self._Q_MAX_ABS_PU= Q_MAX_ABS_PU
    
    @property
    def QV_MODE_ENABLE(self):
        return self._QV_MODE_ENABLE

    @QV_MODE_ENABLE.setter
    def QV_MODE_ENABLE(self, QV_MODE_ENABLE):

        self._QV_MODE_ENABLE = self.check_enabled(QV_MODE_ENABLE)
        if self._QV_MODE_ENABLE:
            self.CONST_Q_MODE_ENABLE, self.QP_MODE_ENABLE, self.CONST_PF_MODE_ENABLE = False, False, False

    @property
    def QV_VREF(self):
        return self._QV_VREF

    @QV_VREF.setter
    def QV_VREF(self, QV_VREF):

        self._QV_VREF = QV_VREF

    @property
    def QV_VREF_AUTO_MODE(self):
        return self._QV_VREF_AUTO_MODE

    @QV_VREF_AUTO_MODE.setter
    def QV_VREF_AUTO_MODE(self, QV_VREF_AUTO_MODE):

        self._QV_VREF_AUTO_MODE = self.check_enabled(QV_VREF_AUTO_MODE)

    @property
    def QV_VREF_TIME(self):
        return self._QV_VREF_TIME

    @QV_VREF_TIME.setter
    def QV_VREF_TIME(self, QV_VREF_TIME):

        self._QV_VREF_TIME = QV_VREF_TIME

    @property
    def QV_CURVE_V2(self):
        return self._QV_CURVE_V2

    @QV_CURVE_V2.setter
    def QV_CURVE_V2(self, QV_CURVE_V2):

        self._QV_CURVE_V2 = QV_CURVE_V2

    @property
    def QV_CURVE_Q2(self):
        return self._QV_CURVE_Q2

    @QV_CURVE_Q2.setter
    def QV_CURVE_Q2(self, QV_CURVE_Q2):

        self._QV_CURVE_Q2 = QV_CURVE_Q2

    @property
    def QV_CURVE_V3(self):
        return self._QV_CURVE_V3

    @QV_CURVE_V3.setter
    def QV_CURVE_V3(self, QV_CURVE_V3):

        self._QV_CURVE_V3 = QV_CURVE_V3

    @property
    def QV_CURVE_Q3(self):
        return self._QV_CURVE_Q3

    @QV_CURVE_Q3.setter
    def QV_CURVE_Q3(self, QV_CURVE_Q3):

        self._QV_CURVE_Q3 = QV_CURVE_Q3

    @property
    def QV_CURVE_V1(self):
        return self._QV_CURVE_V1

    @QV_CURVE_V1.setter
    def QV_CURVE_V1(self, QV_CURVE_V1):

        self._QV_CURVE_V1 = QV_CURVE_V1

    @property
    def QV_CURVE_Q1(self):
        return self._QV_CURVE_Q1

    @QV_CURVE_Q1.setter
    def QV_CURVE_Q1(self, QV_CURVE_Q1):

        self._QV_CURVE_Q1 = QV_CURVE_Q1

    @property
    def QV_CURVE_V4(self):
        return self._QV_CURVE_V4

    @QV_CURVE_V4.setter
    def QV_CURVE_V4(self, QV_CURVE_V4):

        self._QV_CURVE_V4 = QV_CURVE_V4

    @property
    def QV_CURVE_Q4(self):
        return self._QV_CURVE_Q4

    @QV_CURVE_Q4.setter
    def QV_CURVE_Q4(self, QV_CURVE_Q4):

        self._QV_CURVE_Q4 = QV_CURVE_Q4

    @property
    def QV_OLRT(self):
        return self._QV_OLRT

    @QV_OLRT.setter
    def QV_OLRT(self, QV_OLRT):

        self._QV_OLRT = QV_OLRT

    @property
    def QP_MODE_ENABLE(self):
        return self._QP_MODE_ENABLE

    @QP_MODE_ENABLE.setter
    def QP_MODE_ENABLE(self, QP_MODE_ENABLE):

        self._QP_MODE_ENABLE = self.check_enabled(QP_MODE_ENABLE)
        if self._QP_MODE_ENABLE:
            self.CONST_Q_MODE_ENABLE, self.QV_MODE_ENABLE, self.CONST_PF_MODE_ENABLE = False, False, False

    @property
    def QP_CURVE_P3_GEN(self):
        return self._QP_CURVE_P3_GEN

    @QP_CURVE_P3_GEN.setter
    def QP_CURVE_P3_GEN(self, QP_CURVE_P3_GEN):

        self._QP_CURVE_P3_GEN = QP_CURVE_P3_GEN

    @property
    def QP_CURVE_P2_GEN(self):
        return self._QP_CURVE_P2_GEN

    @QP_CURVE_P2_GEN.setter
    def QP_CURVE_P2_GEN(self, QP_CURVE_P2_GEN):

        self._QP_CURVE_P2_GEN = QP_CURVE_P2_GEN

    @property
    def QP_CURVE_P1_GEN(self):
        return self._QP_CURVE_P1_GEN

    @QP_CURVE_P1_GEN.setter
    def QP_CURVE_P1_GEN(self, QP_CURVE_P1_GEN):

        self._QP_CURVE_P1_GEN = QP_CURVE_P1_GEN

    @property
    def QP_CURVE_P1_LOAD(self):
        return self._QP_CURVE_P1_LOAD

    @QP_CURVE_P1_LOAD.setter
    def QP_CURVE_P1_LOAD(self, QP_CURVE_P1_LOAD):

        self._QP_CURVE_P1_LOAD = QP_CURVE_P1_LOAD

    @property
    def QP_CURVE_P2_LOAD(self):
        return self._QP_CURVE_P2_LOAD

    @QP_CURVE_P2_LOAD.setter
    def QP_CURVE_P2_LOAD(self, QP_CURVE_P2_LOAD):

        self._QP_CURVE_P2_LOAD = QP_CURVE_P2_LOAD

    @property
    def QP_CURVE_P3_LOAD(self):
        return self._QP_CURVE_P3_LOAD

    @QP_CURVE_P3_LOAD.setter
    def QP_CURVE_P3_LOAD(self, QP_CURVE_P3_LOAD):

        self._QP_CURVE_P3_LOAD = QP_CURVE_P3_LOAD

    @property
    def QP_CURVE_Q3_GEN(self):
        return self._QP_CURVE_Q3_GEN

    @QP_CURVE_Q3_GEN.setter
    def QP_CURVE_Q3_GEN(self, QP_CURVE_Q3_GEN):

        self._QP_CURVE_Q3_GEN = QP_CURVE_Q3_GEN

    @property
    def QP_CURVE_Q2_GEN(self):
        return self._QP_CURVE_Q2_GEN

    @QP_CURVE_Q2_GEN.setter
    def QP_CURVE_Q2_GEN(self, QP_CURVE_Q2_GEN):

        self._QP_CURVE_Q2_GEN = QP_CURVE_Q2_GEN

    @property
    def QP_CURVE_Q1_GEN(self):
        return self._QP_CURVE_Q1_GEN

    @QP_CURVE_Q1_GEN.setter
    def QP_CURVE_Q1_GEN(self, QP_CURVE_Q1_GEN):

        self._QP_CURVE_Q1_GEN = QP_CURVE_Q1_GEN

    @property
    def QP_CURVE_Q1_LOAD(self):
        return self._QP_CURVE_Q1_LOAD

    @QP_CURVE_Q1_LOAD.setter
    def QP_CURVE_Q1_LOAD(self, QP_CURVE_Q1_LOAD):

        self._QP_CURVE_Q1_LOAD = QP_CURVE_Q1_LOAD

    @property
    def QP_CURVE_Q2_LOAD(self):
        return self._QP_CURVE_Q2_LOAD

    @QP_CURVE_Q2_LOAD.setter
    def QP_CURVE_Q2_LOAD(self, QP_CURVE_Q2_LOAD):

        self._QP_CURVE_Q2_LOAD = QP_CURVE_Q2_LOAD

    @property
    def QP_CURVE_Q3_LOAD(self):
        return self._QP_CURVE_Q3_LOAD

    @QP_CURVE_Q3_LOAD.setter
    def QP_CURVE_Q3_LOAD(self, QP_CURVE_Q3_LOAD):

        self._QP_CURVE_Q3_LOAD = QP_CURVE_Q3_LOAD

    @property
    def QP_RT(self):
        return self._QP_RT

    @QP_RT.setter
    def QP_RT(self, QP_RT):

        self._QP_RT = QP_RT

    @property
    def PV_MODE_ENABLE(self):
        return self._PV_MODE_ENABLE

    @PV_MODE_ENABLE.setter
    def PV_MODE_ENABLE(self, PV_MODE_ENABLE):

        self._PV_MODE_ENABLE = self.check_enabled(PV_MODE_ENABLE)

    @property
    def PV_CURVE_V1(self):
        return self._PV_CURVE_V1

    @PV_CURVE_V1.setter
    def PV_CURVE_V1(self, PV_CURVE_V1):

        self._PV_CURVE_V1 = PV_CURVE_V1

    @property
    def PV_CURVE_P1(self):
        return self._PV_CURVE_P1

    @PV_CURVE_P1.setter
    def PV_CURVE_P1(self, PV_CURVE_P1):

        self._PV_CURVE_P1 = PV_CURVE_P1

    @property
    def PV_CURVE_V2(self):
        return self._PV_CURVE_V2

    @PV_CURVE_V2.setter
    def PV_CURVE_V2(self, PV_CURVE_V2):

        self._PV_CURVE_V2 = PV_CURVE_V2

    @property
    def PV_CURVE_P2(self):
        return self._PV_CURVE_P2

    @PV_CURVE_P2.setter
    def PV_CURVE_P2(self, PV_CURVE_P2):

        self._PV_CURVE_P2 = PV_CURVE_P2

    @property
    def PV_OLRT(self):
        return self._PV_OLRT

    @PV_OLRT.setter
    def PV_OLRT(self, PV_OLRT):

        self._PV_OLRT = PV_OLRT

    @property
    def NP_V_MEAS_UNBALANCE(self):
        return self._NP_V_MEAS_UNBALANCE

    @NP_V_MEAS_UNBALANCE.setter
    def NP_V_MEAS_UNBALANCE(self, NP_V_MEAS_UNBALANCE):

        self._NP_V_MEAS_UNBALANCE = NP_V_MEAS_UNBALANCE

    @property
    def NP_PRIO_OUTSIDE_MIN_Q_REQ(self):
        return self._NP_PRIO_OUTSIDE_MIN_Q_REQ

    @NP_PRIO_OUTSIDE_MIN_Q_REQ.setter
    def NP_PRIO_OUTSIDE_MIN_Q_REQ(self, NP_PRIO_OUTSIDE_MIN_Q_REQ):

        self._NP_PRIO_OUTSIDE_MIN_Q_REQ = NP_PRIO_OUTSIDE_MIN_Q_REQ

    @property
    def NP_Q_CAPABILITY_BY_P_CURVE(self):
        return self._NP_Q_CAPABILITY_BY_P_CURVE

    @NP_Q_CAPABILITY_BY_P_CURVE.setter
    def NP_Q_CAPABILITY_BY_P_CURVE(self, NP_Q_CAPABILITY_BY_P_CURVE):

        self._NP_Q_CAPABILITY_BY_P_CURVE = NP_Q_CAPABILITY_BY_P_CURVE

    @property
    def NP_Q_CAPABILITY_LOW_P(self):
        return self._NP_Q_CAPABILITY_LOW_P

    @NP_Q_CAPABILITY_LOW_P.setter
    def NP_Q_CAPABILITY_LOW_P(self, NP_Q_CAPABILITY_LOW_P):

        self._NP_Q_CAPABILITY_LOW_P = NP_Q_CAPABILITY_LOW_P

    @property
    def NP_EFFICIENCY(self):
        return self._NP_EFFICIENCY

    @NP_EFFICIENCY.setter
    def NP_EFFICIENCY(self, NP_EFFICIENCY):

        self._NP_EFFICIENCY = NP_EFFICIENCY
    
    @property
    def OV2_TRIP_V(self):
        return self._OV2_TRIP_V
    
    @OV2_TRIP_V.setter
    def OV2_TRIP_V(self, OV2_TRIP_V):

        self._OV2_TRIP_V = OV2_TRIP_V
        
    @property
    def OV2_TRIP_T(self):
        return self._OV2_TRIP_T
    
    @OV2_TRIP_T.setter
    def OV2_TRIP_T(self, OV2_TRIP_T):

        self._OV2_TRIP_T = OV2_TRIP_T
        
    @property
    def OV1_TRIP_V(self):
        return self._OV1_TRIP_V
    
    @OV1_TRIP_V.setter
    def OV1_TRIP_V(self, OV1_TRIP_V):

        self._OV1_TRIP_V = OV1_TRIP_V
        
    @property
    def OV1_TRIP_T(self):
        return self._OV1_TRIP_T
    
    @OV1_TRIP_T.setter
    def OV1_TRIP_T(self, OV1_TRIP_T):

        self._OV1_TRIP_T = OV1_TRIP_T
        
    @property
    def UV1_TRIP_V(self):
        return self._UV1_TRIP_V
    
    @UV1_TRIP_V.setter
    def UV1_TRIP_V(self, UV1_TRIP_V):
        self._UV1_TRIP_V = UV1_TRIP_V
        
    @property
    def UV1_TRIP_T(self):
        return self._UV1_TRIP_T
    
    @UV1_TRIP_T.setter
    def UV1_TRIP_T(self, UV1_TRIP_T):
        self._UV1_TRIP_T = UV1_TRIP_T
        
    @property
    def UV2_TRIP_V(self):
        return self._UV2_TRIP_V
    
    @UV2_TRIP_V.setter
    def UV2_TRIP_V(self, UV2_TRIP_V):
        self._UV2_TRIP_V = UV2_TRIP_V
        
    @property
    def UV2_TRIP_T(self):
        return self._UV2_TRIP_T
    
    @UV2_TRIP_T.setter
    def UV2_TRIP_T(self, UV2_TRIP_T):
        self._UV2_TRIP_T = UV2_TRIP_T
    
    @property
    def OF2_TRIP_F(self):
        return self._OF2_TRIP_F
    
    @OF2_TRIP_F.setter
    def OF2_TRIP_F(self, OF2_TRIP_F):
        self._OF2_TRIP_F = OF2_TRIP_F
        
    @property
    def OF2_TRIP_T(self):
        return self._OF2_TRIP_T
        
    @OF2_TRIP_T.setter
    def OF2_TRIP_T(self, OF2_TRIP_T):
        self._OF2_TRIP_T = OF2_TRIP_T

    @property
    def OF1_TRIP_F(self):
        return self._OF1_TRIP_F
    
    @OF1_TRIP_F.setter
    def OF1_TRIP_F(self, OF1_TRIP_F):

        self._OF1_TRIP_F = OF1_TRIP_F
        
    @property
    def OF1_TRIP_T(self):
        return self._OF1_TRIP_T
    
    @OF1_TRIP_T.setter
    def OF1_TRIP_T(self, OF1_TRIP_T):

        self._OF1_TRIP_T = OF1_TRIP_T
        
    @property
    def UF1_TRIP_F(self):
        return self._UF1_TRIP_F
    
    @UF1_TRIP_F.setter
    def UF1_TRIP_F(self, UF1_TRIP_F):

        self._UF1_TRIP_F = UF1_TRIP_F
        
    @property
    def UF1_TRIP_T(self):
        return self._UF1_TRIP_T
    
    @UF1_TRIP_T.setter
    def UF1_TRIP_T(self, UF1_TRIP_T):

        self._UF1_TRIP_T = UF1_TRIP_T
        
    @property
    def UF2_TRIP_F(self):
        return self._UF2_TRIP_F
    
    @UF2_TRIP_F.setter
    def UF2_TRIP_F(self, UF2_TRIP_F):

        self._UF2_TRIP_F = UF2_TRIP_F
        
    @property
    def UF2_TRIP_T (self):
        return self._UF2_TRIP_T 
    
    @UF2_TRIP_T .setter
    def UF2_TRIP_T (self, UF2_TRIP_T ):
        self._UF2_TRIP_T = UF2_TRIP_T 
    
    @property
    def PF_MODE_ENABLE(self):
        return self._PF_MODE_ENABLE
    
    @PF_MODE_ENABLE.setter
    def PF_MODE_ENABLE(self, PF_MODE_ENABLE):
        self._PF_MODE_ENABLE = self.check_enabled(PF_MODE_ENABLE)
    
    @property
    def PF_DBOF(self):
        return self._PF_DBOF
    
    @PF_DBOF.setter
    def PF_DBOF(self, PF_DBOF):
        self._PF_DBOF = PF_DBOF
    
    @property
    def PF_DBUF(self):
        return self._PF_DBUF
    
    @PF_DBUF.setter
    def PF_DBUF(self, PF_DBUF):

        self._PF_DBUF = PF_DBUF
    
    @property
    def PF_KOF(self):
        return self._PF_KOF
    
    @PF_KOF.setter
    def PF_KOF(self, PF_KOF):

        self._PF_KOF = PF_KOF
    
    @property
    def PF_KUF(self):
        return self._PF_KUF
    
    @PF_KUF.setter
    def PF_KUF(self, PF_KUF):

        self._PF_KUF = PF_KUF
    
    @property
    def PF_OLRT(self):
        return self._PF_OLRT
    
    @PF_OLRT.setter
    def PF_OLRT(self, PF_OLRT):

        self._PF_OLRT = PF_OLRT
        
    @property
    def STATUS_INIT(self):
        return self._STATUS_INIT
    
    @STATUS_INIT.setter
    def STATUS_INIT(self, STATUS_INIT):
        if type(STATUS_INIT) is str:
            if(STATUS_INIT.upper() == "ON") or (STATUS_INIT.upper() == "ENABLED"):
                self._STATUS_INIT = True
            elif(STATUS_INIT.upper() == "OFF") or (STATUS_INIT.upper() == "DISABLED"):
                self._STATUS_INIT = False
            else:
                print('STATUS_INIT value not valid')
        elif type(STATUS_INIT) is bool:
            self._STATUS_INIT = STATUS_INIT
        else:
            print('STATUS_INIT value not valid')


    @property
    def AP_RT(self):
        return self._AP_RT

    @AP_RT.setter
    def AP_RT(self, AP_RT):

        self._AP_RT = AP_RT


if __name__ == "__main__":
    import pathlib
    import os

    script_path = pathlib.Path(os.path.dirname(__file__)).parent

    as_file_path = script_path.joinpath("commonfileformat", "Parameters", "AS-with std-values.csv")
    model_file_path = script_path.joinpath("commonfileformat", "Parameters", "Model-parameters.csv")
    
    print(as_file_path)
    print(model_file_path)
    
    file_ss_obj = DERCommonFileFormat(as_file_path, model_file_path)
<template>
    <div class="box-contain">
        <el-card style="width:100vw;margin:20px;">
            <div id="box1" class="box">
                <el-row>
                    <el-col :span="12">
                        <!-- 子域模块 -->
                        <div style="height:600px;width:100%;">
                            <div
                                style="background-color:#a6d9f4;border-radius: 20px;margin:5px;padding:10px;text-align:center">
                                <el-cascader v-model="value_subDomain" :options="options_subDomain" filterable clearable
                                    @change="searchModelNamesDetails" placeholder="请选择">
                                </el-cascader>
                                <el-switch v-model="value1" active-value="opensubDomain" inactive-value="offsubDomain"
                                    @change="changeclear" style="margin-left: 20px">
                                </el-switch>
                            </div>
                            <el-row>
                                <el-col :span="6" style="text-align:center">
                                    <span
                                        style="font-size: large;margin-top: 5px;margin-bottom: 10px ;display:inline-block;color: #7BC9F4;">子域属性</span>
                                    <br>
                                    <hr style="border-top: 1px solid #7BC9F4;">
                                    <br>
                                    <el-tree :data="tableModelsubDomain" @node-click="handleNodeClick">
                                    </el-tree>
                                </el-col>
                                <el-col :span="18">
                                    <div id="GraphsubDomain" style="width:100%;height:520px" v-if="show_subDomain">

                                    </div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-col>
                    <!-- 信息模型部分 -->
                    <el-col :span="12">
                        <div style="height:600px;width:100%;">
                            <div
                                style="background-color:#a6d9f4; border-radius: 20px; margin: 5px; padding: 10px; display: flex; align-items: center;">

                                <el-select v-model="selectedModelName" filterable @change="searchModelName"
                                    placeholder="请选择查询模型" style="margin-left:10%">
                                    <el-option v-for="item in optionsOfModelName" :key="item.value" :label="item.label"
                                        :value="item.value"></el-option>
                                </el-select>

                                <span style="margin-left: 10%;">信息模型</span>

                                <el-switch v-model="value2" active-value="openModelName" inactive-value="offModelName"
                                    @change="changeclear" style="margin-left: 10%;"></el-switch>

                            </div>

                            <div id="chartIdModel" style="width:100%; height:520px" v-if="show_DataModel">

                            </div>
                        </div>
                    </el-col>
                </el-row>
            </div>

            <div id="box2" class="box">
                <el-row>
                    <!-- 演化 -->
                    <el-col :span="12">
                        <div style="height:600px;width:100%">
                            <div
                                style="background-color:#a6d9f4; border-radius: 20px; margin: 5px; padding: 10px; height: 60px; display: flex; align-items: center; justify-content: center;">
                                <span style="margin-left:20px;">演化</span>
                                <el-switch v-model="value3" active-value="openEvolution" inactive-value="offEvolution"
                                    @change="changeclear" style="margin-left: 150px;">
                                </el-switch>
                            </div>
                            <div id="GraphEvolution" style="width:100%;height:520px" v-if="show_Evolution">

                            </div>
                        </div>
                    </el-col>
                    <!-- 表属性 -->
                    <el-dialog title="修改表属性" :visible.sync="dialogFormtable" width="20%">
                        <el-form :model="formtable">
                            <el-form-item label="表属性名称">
                                <el-input v-model="formtable.name" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormtable = false">取 消</el-button>
                            <el-button type="primary" @click="modifytable">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- 表属性值 -->
                    <el-dialog title="修改表属性值" :visible.sync="dialogFormtablevalue" width="20%">
                        <el-form :model="formtablevalue">
                            <el-form-item label="表属性值名称">
                                <el-input v-model="formtablevalue.name" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormtablevalue = false">取 消</el-button>
                            <el-button type="primary" @click="modifytablevalue">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- MDR -->
                    <el-col :span="12">
                        <div style="height:600px;width:100%">
                            <div
                                style="background-color:#a6d9f4; border-radius: 20px; margin: 5px; padding: 10px; display: flex; align-items: center;">
                                <el-select v-model="valueMDRname" placeholder="请选择数据元" style="margin-left:10%"
                                    @change="getMDRGraph">
                                    <el-option v-for="item in optionsMDR" :key="item.value" :label="item.label"
                                        :value="item.value">
                                    </el-option>
                                </el-select>
                                <span style="margin-left:10%">MDR</span>
                                <el-switch v-model="value4" active-value="openMDR" inactive-value="offMDR"
                                    @change="changeclear" style="margin-left: 10%;">
                                </el-switch>
                            </div>
                            <div id="MDRGraph" style="width:100%; height:520px" v-if="show_MDR">
                            </div>
                        </div>
                    </el-col>
                    <!-- 对象类 -->
                    <el-dialog title="修改对象类" :visible.sync="dialogFormclassname" width="40%">
                        <el-form :model="formtablevalueMDR.Datavalue">
                            <el-form-item label="对象类:">
                                <el-input v-model="formtablevalueMDR.Datavalue.name" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="标识符:">
                                <el-input v-model="formtablevalueMDR.Datavalue.identifier" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="描述:">
                                <el-input v-model="formtablevalueMDR.Datavalue.describe" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="注册状态:">
                                <el-input v-model="formtablevalueMDR.Datavalue.status" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <el-input v-model="formtablevalueMDR.Datavalue.time" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="版本:">
                                <el-input v-model="formtablevalueMDR.Datavalue.version" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建人员ID">
                                <el-input v-model="formtablevalueMDR.Datavalue.personId" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="创建单位:">
                                <el-input v-model="formtablevalueMDR.Datavalue.department" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormclassname = false">取 消</el-button>
                            <el-button type="primary" @click="modifyclassname">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- 属性 -->
                    <el-dialog title="修改属性" :visible.sync="dialogFormproperty" width="40%">
                        <el-form :model="formtablevalueMDR.Datavalue">
                            <el-form-item label="属性:">
                                <el-input v-model="formtablevalueMDR.Datavalue.name" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="标识符:">
                                <el-input v-model="formtablevalueMDR.Datavalue.identifier" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="描述:">
                                <el-input v-model="formtablevalueMDR.Datavalue.describe" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="注册状态:">
                                <el-input v-model="formtablevalueMDR.Datavalue.status" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <el-input v-model="formtablevalueMDR.Datavalue.time" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="版本:">
                                <el-input v-model="formtablevalueMDR.Datavalue.version" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建人员ID">
                                <el-input v-model="formtablevalueMDR.Datavalue.personId" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="创建单位:">
                                <el-input v-model="formtablevalueMDR.Datavalue.department" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormproperty = false">取 消</el-button>
                            <el-button type="primary" @click="modifyproperty">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- 概念域 -->
                    <el-dialog title="修改概念域" :visible.sync="dialogFormConceptualDomain" width="40%">
                        <el-form :model="formtablevalueMDR.Datavalue">
                            <el-form-item label="概念域:">
                                <el-input v-model="formtablevalueMDR.Datavalue.name" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="标识符:">
                                <el-input v-model="formtablevalueMDR.Datavalue.identifier" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="描述:">
                                <el-input v-model="formtablevalueMDR.Datavalue.describe" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="注册状态:">
                                <el-input v-model="formtablevalueMDR.Datavalue.status" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <el-input v-model="formtablevalueMDR.Datavalue.time" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="版本:">
                                <el-input v-model="formtablevalueMDR.Datavalue.version" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建人员ID">
                                <el-input v-model="formtablevalueMDR.Datavalue.personId" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="创建单位:">
                                <el-input v-model="formtablevalueMDR.Datavalue.department" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <el-divider content-position="center">值含义信息</el-divider>
                        <div v-if="formtablevalueMDR.dialogDataValueMenings">
                            <el-descriptions v-for="(item, index) in formtablevalueMDR.dialogDataValueMenings" border
                                style="margin-bottom: 20px;" :key="index">
                                <el-descriptions-item label="值含义">{{ item.name }}</el-descriptions-item>
                                <el-descriptions-item label="标识符">{{ item.identifier }}</el-descriptions-item>
                                <el-descriptions-item label="创建时间">{{ item.time }}</el-descriptions-item>
                                <el-descriptions-item label="注册状态">{{ item.status }}</el-descriptions-item>
                                <el-descriptions-item label="版本">{{ item.version }}</el-descriptions-item>
                            </el-descriptions>
                        </div>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormConceptualDomain = false">取 消</el-button>
                            <el-button type="primary" @click="modifyConceptualDomain">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- 数据元概念 -->
                    <el-dialog title="修改数据元概念" :visible.sync="dialogFormDataElementConcept" width="40%">
                        <el-form :model="formtablevalueMDR.Datavalue">
                            <el-form-item label="数据元概念:">
                                <el-input v-model="formtablevalueMDR.Datavalue.name" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="标识符:">
                                <el-input v-model="formtablevalueMDR.Datavalue.identifier" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="描述:">
                                <el-input v-model="formtablevalueMDR.Datavalue.describe" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="注册状态:">
                                <el-input v-model="formtablevalueMDR.Datavalue.status" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <el-input v-model="formtablevalueMDR.Datavalue.time" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="版本:">
                                <el-input v-model="formtablevalueMDR.Datavalue.version" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建人员ID">
                                <el-input v-model="formtablevalueMDR.Datavalue.personId" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="创建单位:">
                                <el-input v-model="formtablevalueMDR.Datavalue.department" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormDataElementConcept = false">取 消</el-button>
                            <el-button type="primary" @click="modifyDataElementConcept">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- 值域 -->
                    <el-dialog title="修改值域" :visible.sync="dialogFormValueDomain" width="40%">
                        <el-form :model="formtablevalueMDR.Datavalue">
                            <el-form-item label="值域:">
                                <el-input v-model="formtablevalueMDR.Datavalue.name" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="标识符:">
                                <el-input v-model="formtablevalueMDR.Datavalue.identifier" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="描述:">
                                <el-input v-model="formtablevalueMDR.Datavalue.describe" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="注册状态:">
                                <el-input v-model="formtablevalueMDR.Datavalue.status" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <el-input v-model="formtablevalueMDR.Datavalue.time" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="版本:">
                                <el-input v-model="formtablevalueMDR.Datavalue.version" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建人员ID">
                                <el-input v-model="formtablevalueMDR.Datavalue.personId" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="创建单位:">
                                <el-input v-model="formtablevalueMDR.Datavalue.department" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <el-divider content-position="center">可允许值信息</el-divider>
                        <div v-if="formtablevalueMDR.dialogDataValueMenings">
                            <el-descriptions v-for="(item, index) in formtablevalueMDR.dialogDataValueMenings" border
                                style="margin-bottom: 20px;" :column="2" :key="index">
                                <el-descriptions-item label="可允许值">{{ item.PEVName }}</el-descriptions-item>
                                <el-descriptions-item label="标识符">{{ item.PEVIdentifier }}</el-descriptions-item>
                                <el-descriptions-item label="值含义">{{ item.VLMName }}</el-descriptions-item>
                                <el-descriptions-item label="标识符">{{ item.VLMIdentifier }}</el-descriptions-item>
                            </el-descriptions>
                        </div>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormValueDomain = false">取 消</el-button>
                            <el-button type="primary" @click="modifyValueDomain">确 定</el-button>
                        </div>
                    </el-dialog>
                    <!-- 数据元 -->
                    <el-dialog title="修改数据元" :visible.sync="dialogFormDataElement" width="40%">
                        <el-form :model="formtablevalueMDR.Datavalue">
                            <el-form-item label="数据元:">
                                <el-input v-model="formtablevalueMDR.Datavalue.name" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="标识符:">
                                <el-input v-model="formtablevalueMDR.Datavalue.identifier" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="描述:">
                                <el-input v-model="formtablevalueMDR.Datavalue.describe" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="注册状态:">
                                <el-input v-model="formtablevalueMDR.Datavalue.status" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间:">
                                <el-input v-model="formtablevalueMDR.Datavalue.time" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="版本:">
                                <el-input v-model="formtablevalueMDR.Datavalue.version" autocomplete="off"
                                    :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="创建人员ID">
                                <el-input v-model="formtablevalueMDR.Datavalue.personId" autocomplete="off"></el-input>
                            </el-form-item>
                            <el-form-item label="创建单位:">
                                <el-input v-model="formtablevalueMDR.Datavalue.department" autocomplete="off"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormDataElement = false">取 消</el-button>
                            <el-button type="primary" @click="modifyDataElement">确 定</el-button>
                        </div>
                    </el-dialog>
                </el-row>
            </div>
            <!-- 子域删除模块 -->
            <div class="delete_subDomain">
                <div class="delete_subDomain_title" style="height: 60px;background-color:#a6d9f4; border-radius: 20px;
                 padding: 10px; display: flex; align-items: center;">
                    <span style="font-size: 20px;margin-left: 45%;">子 域 删 除</span>
                </div>

                <el-main>
                    <el-card>
                        <el-row class="row-with-divider">
                            <el-col :span="8">
                                <el-form ref="deletetableForm" :model="deletetableName" label-width="auto"
                                    style="margin-top: 20px;margin-left: 20px;margin-right: 20px">
                                    <div style="text-align: center;">
                                        <h4>删 除 表</h4>
                                    </div>
                                    <br>
                                    <el-form-item label="表名称:">
                                        <template>
                                            <el-select v-model="deletetableName.value" filterable default-first-option
                                                placeholder="请选择要删除的表:">
                                                <el-option v-for="item in options_table" :key="item.value"
                                                    :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-form-item>
                                    <el-form-item>
                                        <el-button @click="DeletetableName">删除表</el-button>
                                        <el-button type="danger" @click="resetForm">重置</el-button>
                                    </el-form-item>
                                </el-form>
                            </el-col>
                            <el-col :span="8">
                                <el-form ref="deletetablepropertyForm" :model="deletetableName1" label-width="auto"
                                    style="margin-top: 20px;margin-left: 20px;margin-right: 20px">
                                    <div style="text-align: center;">
                                        <h4>删 除 表 属 性</h4>
                                    </div>
                                    <br>
                                    <el-form-item label="表名称:">
                                        <template>
                                            <el-select v-model="deletetableName1.value" filterable default-first-option
                                                placeholder="请选择要删除的表:" @change="searchtableProperty">
                                                <el-option v-for="item in options_table" :key="item.value"
                                                    :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-form-item>
                                    <el-form-item label="表属性:">
                                        <template>
                                            <el-select v-model="deletetablePropertyName.value" filterable
                                                default-first-option placeholder="请选择要删除的表属性:">
                                                <el-option v-for="item in options_tableproperty" :key="item.value"
                                                    :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-form-item>
                                    <el-form-item>
                                        <el-button @click="DeletetablePropertyName">删除表属性</el-button>
                                        <el-button type="danger" @click="resetForm">重置</el-button>
                                    </el-form-item>
                                </el-form>
                            </el-col>
                            <el-col :span="8">
                                <el-form ref="deletetablepropertyValueForm" :model="deletetableName2" label-width="auto"
                                    style="margin-top: 20px;margin-left: 20px;">
                                    <div style="text-align: center;">
                                        <h4>删 除 表 属 性 值</h4>
                                    </div>
                                    <br>
                                    <el-form-item label="表名称:">
                                        <template>
                                            <el-select v-model="deletetableName2.value" filterable default-first-option
                                                placeholder="请选择要删除的表:" @change="searchtablePropertyValue">
                                                <el-option v-for="item in options_table" :key="item.value"
                                                    :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-form-item>
                                    <el-form-item label="表属性值:">
                                        <template>
                                            <el-select v-model="deletetablePropertyValueName.value" filterable
                                                default-first-option placeholder="请选择要删除的表属性值:">
                                                <el-option v-for="item in options_tablepropertyValue" :key="item.value"
                                                    :label="item.label" :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </template>
                                    </el-form-item>
                                    <el-form-item>
                                        <el-button @click="DeletetablePropertyValueName"
                                            style="font-size: 10px;">删除表属性值</el-button>
                                        <el-button type="danger" @click="resetForm">重置</el-button>
                                    </el-form-item>
                                </el-form>
                            </el-col>
                        </el-row>
                    </el-card>
                </el-main>
            </div>
            <div class="buttom">
                <el-steps :active="active" finish-status="success" align-center
                    style="background-color:#c9e8f8;border-radius: 20px;margin:5px;padding:20px">
                    <el-step title="步骤 1" description="信息模型演化"></el-step>
                    <el-step title="步骤 2" description="MDR演化"></el-step>
                    <el-step title="步骤 3" description="子域到MDR的映射演化"></el-step>
                </el-steps>
                <div style="display: flex; justify-content: center;">
                    <el-button style="margin-top: 20px;" @click="front">上一步</el-button>
                    <el-button style="margin-top: 20px;" @click="next">下一步</el-button>
                </div>
                <div style="display: flex; justify-content: center; margin-top:40px">
                    <el-card style="max-width:80vw">
                        <!-- 信息模型注册 -->
                        <div v-show="showinformation_model">
                            <div style="display: flex; justify-content: space-between; width: 100%;">
                                <el-button type="success" size="mini" @click="changeShowAddModelClassTable"
                                    style="flex: 1;">注册类</el-button>
                                <el-button type="success" size="mini" @click="changeShowAddModelPropertyTable"
                                    style="flex: 1;">注册属性</el-button>
                                <el-button type="success" size="mini" @click="changeShowAddModelRelationTable"
                                    style="flex: 1;">注册关系</el-button>
                                <el-button type="danger" size="mini" @click="changeShowDeleteModelPropertyTable"
                                    style="flex: 1;">属性删除</el-button>
                            </div>

                            <!-- 注册类 -->
                            <el-form ref="addModelClassTableForm" :model="addClassName" label-width="auto"
                                style="margin-top: 20px;" v-show="showAddModelClassTable">
                                <div style="text-align: center;">
                                    <h5>添加类</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true"></el-input>
                                </el-form-item>
                                <el-form-item label="类名:">
                                    <el-input v-model="addClassName.class_name" clearable placeholder="请输入内容"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="success" @click="addClass">注册类</el-button>
                                    <el-button type="danger" @click="resetFormModel">重置</el-button>
                                </el-form-item>
                            </el-form>

                            <!-- 注册属性 -->
                            <el-form ref="addModelPropertyTableForm" :model="addPropertyName" label-width="auto"
                                style="margin-top: 20px;" v-show="showAddModelPropertyTable">
                                <div style="text-align: center;">
                                    <h5>添加属性</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true" clearable
                                        placeholder="请输入内容"></el-input>
                                </el-form-item>
                                <el-form-item label="类:">
                                    <template>
                                        <el-select v-model="addPropertyName.class_name" filterable default-first-option
                                            placeholder="请选择类:">
                                            <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-form-item>
                                <div v-for="(property, index) in addPropertyName.property_names" :key="index">
                                    <el-form-item :label="`属性名 ${index + 1}`">
                                        <div style="display: flex; align-items: center;">
                                            <el-input v-model="addPropertyName.property_names[index]" clearable
                                                placeholder="请输入内容"></el-input>
                                            <el-button icon="el-icon-delete" @click="removePropertyItem(index)"
                                                circle></el-button>
                                        </div>
                                    </el-form-item>
                                </div>
                                <el-form-item>
                                    <el-button icon="el-icon-plus" @click="addPropertyItem" circle></el-button>
                                    <el-button type="success" @click="addProperty">注册属性</el-button>
                                    <el-button type="danger" @click="resetFormModel">重置</el-button>
                                </el-form-item>
                            </el-form>

                            <!-- 注册关系 -->
                            <el-form ref="addModelRelaionTableForm" :model="addRelationData" label-width="auto"
                                style="margin-top: 20px;" v-show="showAddModelRelationTable">
                                <div style="text-align: center;">
                                    <h5>添加关系</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true"></el-input>
                                </el-form-item>
                                <el-form-item label="类1:">
                                    <template>
                                        <el-select v-model="addRelationData.class_name1" filterable default-first-option
                                            placeholder="请选择类:">
                                            <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-form-item>
                                <el-form-item label="类 2:">
                                    <template>
                                        <el-select v-model="addRelationData.class_name2" filterable default-first-option
                                            placeholder="请选择类:">
                                            <el-option v-for="item in optionsOfModelClassName" :key="item.value"
                                                :label="item.label" :value="item.value">
                                            </el-option>
                                        </el-select>
                                    </template>
                                </el-form-item>
                                <el-form-item label="关系:">
                                    <el-input v-model="addRelationData.relation" clearable></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-button type="success" @click="addRelation">注册关系</el-button>
                                    <el-button type="danger" @click="resetFormModel">重置</el-button>
                                </el-form-item>
                            </el-form>

                            <!-- 属性删除 -->
                            <el-form ref="deleteModelPropertyTableForm" :model="deleteProperty" label-width="auto"
                                style="margin-top: 20px;" v-show="showDeleteModelPropertyTable">
                                <div style="text-align: center;">
                                    <h5>属性删除</h5>
                                </div>
                                <br>
                                <el-form-item label="模型名称:">
                                    <el-input v-model="selectedModelName" :disabled="true"></el-input>
                                </el-form-item>
                                <el-form-item label="属性名称:">
                                    <template>
                                        <el-cascader v-model="deleteProperty.deletePropertyName"
                                            :options="optionsOfModelPropertyName" filterable clearable placeholder="请选择">
                                        </el-cascader>
                                    </template>
                                </el-form-item>
                                <el-form-item>
                                    <el-button @click="DeletePropertyName">删除属性</el-button>
                                    <el-button type="danger" @click="resetFormModel">重置</el-button>
                                </el-form-item>
                            </el-form>
                        </div>
                        <!-- MDR注册 -->
                        <div v-show="showMDRregister">
                            <el-row>
                                <el-col :span="8">
                                    <el-aside>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success" @click="changeShowObjectClass">
                                                    对象类
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success" @click="changeShowProperty">
                                                    属性
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success"
                                                    @click="changeShowConceptualDomain">
                                                    概念域
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success"
                                                    @click="changeShowDataElementConcept">
                                                    数据元概念
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success" @click="changeShowValueDomain">
                                                    值域
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success" @click="changeShowDataElement">
                                                    数据元
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success" @click="changeShowDataValue">
                                                    新增值域可枚举值
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col>
                                                <el-button class="button" type="success"
                                                    @click="changeShowConceptualDomainValue">
                                                    新增概念域值含义
                                                </el-button>
                                            </el-col>
                                        </el-row>
                                    </el-aside>
                                </el-col>
                                <el-col :span="16">
                                    <el-main style="text-align: center">
                                        <!-- 对象类注册 -->
                                        <div v-show="showObjectClass" class="showbox">
                                            <div>
                                                <h3>对象类注册</h3>
                                            </div>
                                            <div>
                                                <el-form ref="registerObjectClassForm" :model="registerObjectClassData"
                                                    label-width="auto" style="margin-top: 20px; width: 90%; "
                                                    v-show="showObjectClass">
                                                    <el-form-item label="名称:" prop="name">
                                                        <el-input v-model="registerObjectClassData.name" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="描述:" prop="describe">
                                                        <el-input v-model="registerObjectClassData.describe" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建人员ID:" prop="personId">
                                                        <el-input v-model="registerObjectClassData.personId" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建单位:" prop="department">
                                                        <el-input v-model="registerObjectClassData.department" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-button type="primary" @click="registerObjectClass">注册</el-button>
                                                    <el-button type="danger"
                                                        @click="resetFormMDR('registerObjectClassForm')">重置</el-button>
                                                </el-form>
                                            </div>
                                        </div>

                                        <!-- 属性注册 -->
                                        <div v-show="showProperty" class="showbox">
                                            <div>
                                                <h3>属性注册</h3>
                                            </div>
                                            <div>
                                                <el-form ref="registerPropertyForm" :model="registerPropertyData"
                                                    label-width="auto" style="margin-top: 20px; width: 90%;"
                                                    v-show="showProperty">
                                                    <el-form-item label="名称:" prop="name">
                                                        <el-input v-model="registerPropertyData.name" width="20px" clearable
                                                            placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="描述:" prop="describe">
                                                        <el-input v-model="registerPropertyData.describe" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建人员ID:" prop="personId">
                                                        <el-input v-model="registerPropertyData.personId" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建单位:" prop="department">
                                                        <el-input v-model="registerPropertyData.department" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-button type="primary" @click="registerProperty">注册</el-button>
                                                    <el-button type="danger"
                                                        @click="resetFormMDR('registerPropertyForm')">重置</el-button>
                                                </el-form>
                                            </div>
                                        </div>

                                        <!-- 概念域注册 -->
                                        <div v-show="showConceptualDomain" class="showbox">
                                            <div>
                                                <h3 style="margin-bottom: 20px;">概念域注册</h3>
                                            </div>
                                            <div>
                                                <!-- {% raw %} -->
                                                <el-form :model="registerConceptualDomainData"
                                                    ref="registerConceptualDomainForm" label-width="auto"
                                                    class="demo-dynamic" style="width: 90%;" v-show="showConceptualDomain">
                                                    <el-form-item label="名称:" prop="name">
                                                        <el-input v-model="registerConceptualDomainData.name" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="描述:" prop="describe">
                                                        <el-input v-model="registerConceptualDomainData.describe"
                                                            width="20px" clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建人员ID:" prop="personId">
                                                        <el-input v-model="registerConceptualDomainData.personId"
                                                            width="20px" clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建单位:" prop="department">
                                                        <el-input v-model="registerConceptualDomainData.department"
                                                            width="20px" clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item
                                                        v-for="(valueMeaning, index) in registerConceptualDomainData.valueMeanings"
                                                        :label="'值含义:' + (startIndex + index)" :key="startIndex + index"
                                                        prop="'valueMeaning'  + (startIndex + index)">
                                                        <div style="display: flex; align-items: center;">
                                                            <el-input
                                                                v-model="registerConceptualDomainData.valueMeanings[index]"
                                                                width="20px" clearable placeholder="请输入内容"></el-input>
                                                            <el-button icon="el-icon-delete" style="margin-left: 10px;"
                                                                @click.prevent="removeValueMeaning(valueMeaning)"
                                                                circle></el-button>
                                                        </div>
                                                    </el-form-item>
                                                    <el-form-item>
                                                        <el-button type="primary"
                                                            @click="registerConceptualDomain">注册</el-button>
                                                        <el-button @click="addValueMeaning"
                                                            icon="el-icon-plus">新增值含义</el-button>
                                                        <el-button type="danger"
                                                            @click="resetFormMDR('registerConceptualDomainForm')">重置</el-button>
                                                    </el-form-item>
                                                </el-form>
                                                <!-- {% endraw %} -->
                                            </div>
                                        </div>

                                        <!-- 数据元概念注册 -->
                                        <div v-show="showDataElementConcept" class="showbox">
                                            <div>
                                                <h3>数据元概念注册</h3>
                                            </div>
                                            <div>
                                                <el-form ref="registerDataElementConceptForm"
                                                    :model="registerDataElementConceptData" label-width="auto"
                                                    style="margin-top: 20px; width:90%;" v-show="showDataElementConcept">
                                                    <el-form-item label="名称:" prop="name">
                                                        <el-input v-model="registerDataElementConceptData.name" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="描述:" prop="describe">
                                                        <el-input v-model="registerDataElementConceptData.describe"
                                                            width="20px" clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建人员ID:" prop="personId">
                                                        <el-input v-model="registerDataElementConceptData.personId"
                                                            width="20px" clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建单位:" prop="department">
                                                        <el-input v-model="registerDataElementConceptData.department"
                                                            width="20px" clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="对象类:" prop="objectClass">
                                                        <el-select v-model="registerDataElementConceptData.objectClass"
                                                            filterable remote @focus="searchObjectClass"
                                                            :loading="objectClassLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in objectClassOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>

                                                    <el-form-item label="属性" prop="property">
                                                        <el-select v-model="registerDataElementConceptData.property"
                                                            filterable remote @focus="searchProperty"
                                                            :loading="propertyLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in propertyOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>

                                                    <el-form-item label="概念域" prop="conceptualDomain">
                                                        <el-select v-model="registerDataElementConceptData.conceptualDomain"
                                                            filterable remote @focus="searchConceptualDomain"
                                                            :loading="conceptualDomainLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in conceptualDomainOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>

                                                    <el-form-item>
                                                        <el-button type="primary"
                                                            @click="registerDataElementConcept">注册</el-button>
                                                        <el-button type="danger"
                                                            @click="resetFormMDR('registerDataElementConceptForm')">重置</el-button>
                                                    </el-form-item>
                                                </el-form>
                                            </div>
                                        </div>

                                        <!-- 值域注册 -->
                                        <div v-show="showValueDomain" class="showbox" style="width:30vw">
                                            <div>
                                                <h3>值域注册</h3>
                                            </div>
                                            <div>
                                                <el-form ref="registerValueDomainForm" :model="registerValueDomainData"
                                                    label-width="auto" style="margin-top: 20px; width: 90%;"
                                                    v-show="showValueDomain">
                                                    <el-form-item label="名称:" prop="name">
                                                        <el-input v-model="registerValueDomainData.name" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="描述:" prop="describe">
                                                        <el-input v-model="registerValueDomainData.describe" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建人员ID:" prop="personId">
                                                        <el-input v-model="registerValueDomainData.personId" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建单位:" prop="department">
                                                        <el-input v-model="registerValueDomainData.department" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="不可枚举:" prop="indefinite">
                                                        <el-input v-model="registerValueDomainData.indefinite" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>

                                                    <el-form-item label="可枚举:" prop="enumerable">
                                                        <div v-for="(item, index) in registerValueDomainData.enumerable"
                                                            :key="index">
                                                            <el-form-item>
                                                                <div style="align-items:left;">
                                                                    <div style="width: 100%; display: flex;">
                                                                        <el-input v-model="item.value" placeholder="请输入值"
                                                                            clearable></el-input>
                                                                        <el-input v-model="item.num" placeholder="请输入组号"
                                                                            clearable></el-input>
                                                                    </div>
                                                                    <div style="align-items: center; display: flex;">
                                                                        <el-select v-model="item.valueMeaning" filterable
                                                                            remote @focus="searchValueMeanings"
                                                                            :loading="valueMeaningsLoading"
                                                                            :value-key="'label'">
                                                                            <!-- {% raw %} -->
                                                                            <el-option
                                                                                v-for="(option, index) in valueMeaningsOptions"
                                                                                :key="index" :label="option.label"
                                                                                :value="option.value" placeholder="值含义">
                                                                                <span style="float: left">{{ option.label
                                                                                }}</span>
                                                                                <span
                                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                                        option.value }}</span>
                                                                            </el-option>
                                                                            <!-- {% endraw %} -->
                                                                        </el-select>
                                                                        <el-button icon="el-icon-delete"
                                                                            @click.prevent="removePermissibleValues(item)"></el-button>
                                                                    </div>
                                                                </div>
                                                            </el-form-item>
                                                        </div>
                                                        <div>
                                                            <el-button type="primary" icon="el-icon-plus"
                                                                @click="addValueDomainItem">添加</el-button>
                                                        </div>
                                                    </el-form-item>
                                                    <el-form-item label="概念域" prop="conceptualDomain">
                                                        <el-select v-model="registerValueDomainData.conceptualDomain"
                                                            filterable remote @focus="searchConceptualDomain"
                                                            :loading="conceptualDomainLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in conceptualDomainOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>

                                                    <el-form-item>
                                                        <el-button type="primary"
                                                            @click="registerValueDomain">注册</el-button>
                                                        <el-button type="danger"
                                                            @click="resetFormMDR('registerValueDomainForm')">重置</el-button>
                                                    </el-form-item>
                                                </el-form>
                                            </div>
                                        </div>

                                        <!-- 数据元注册 -->
                                        <div v-show="showDataElement" class="showbox">
                                            <div>
                                                <h3>数据元注册</h3>
                                            </div>
                                            <div>
                                                <el-form ref="registerDataElementForm" :model="registerDataElementData"
                                                    label-width="auto" style="margin-top: 20px; width: 90%;"
                                                    v-show="showDataElement">
                                                    <el-form-item label="名称:" prop="name">
                                                        <el-input v-model="registerDataElementData.name" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="描述:" prop="describe">
                                                        <el-input v-model="registerDataElementData.describe" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建人员ID:" prop="personId">
                                                        <el-input v-model="registerDataElementData.personId" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="创建单位:" prop="department">
                                                        <el-input v-model="registerDataElementData.department" width="20px"
                                                            clearable placeholder="请输入内容"></el-input>
                                                    </el-form-item>
                                                    <el-form-item label="数据元概念:" prop="dataElementConcept">
                                                        <el-select v-model="registerDataElementData.dataElementConcept"
                                                            filterable remote @focus="searchDataElementConcept"
                                                            :loading="dataElementConceptLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in dataElementConceptOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>
                                                    <el-form-item label="值域:" prop="valueDomain">
                                                        <el-select v-model="registerDataElementData.valueDomain" filterable
                                                            remote @focus="searchValueDomain" :loading="valueDomainLoading"
                                                            :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in valueDomainOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>
                                                    <el-form-item>
                                                        <el-button type="primary"
                                                            @click="registerDataElement">注册</el-button>
                                                        <el-button type="danger"
                                                            @click="resetFormMDR('registerDataElementForm')">重置</el-button>
                                                    </el-form-item>
                                                </el-form>
                                            </div>
                                        </div>

                                        <!-- 新增可允许值 -->
                                        <div v-show="showValueDomainValue" class="showbox" style="width:30vw">
                                            <div>
                                                <h3>值域新增可允许值</h3>
                                            </div>
                                            <div>
                                                <el-form ref="registerValueDomainFormvalue"
                                                    :model="registerValueDomainDataValuelabel" label-width="auto"
                                                    style="margin-top: 20px; width: 90%;" v-show="showValueDomainValue">
                                                    <el-form-item label="值域:" prop="registerDomainFormValue">
                                                        <el-select
                                                            v-model="registerValueDomainDataValuelabel.registerDomainFormValue"
                                                            filterable remote @focus="searchDataDomain"
                                                            :loading="DataDomainLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in DataDomainOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>

                                                    <el-form-item label="可枚举:" prop="enumerable">
                                                        <div v-for="(item, index) in registerValueDomainData.enumerable"
                                                            :key="index">
                                                            <el-form-item>
                                                                <div style="align-items:left;">
                                                                    <div style="width: 100%; display: flex;">
                                                                        <el-input v-model="item.value" placeholder="请输入值"
                                                                            clearable></el-input>
                                                                        <el-input v-model="item.num" placeholder="请输入组号"
                                                                            clearable></el-input>
                                                                    </div>
                                                                    <div style="align-items: center; display: flex;">
                                                                        <el-select v-model="item.valueMeaning" filterable
                                                                            remote @focus="searchValueMeanings"
                                                                            :loading="valueMeaningsLoading"
                                                                            :value-key="'label'">

                                                                            <el-option
                                                                                v-for="(option, index) in valueMeaningsOptions"
                                                                                :key="index" :label="option.label"
                                                                                :value="option.value" placeholder="值含义">
                                                                                <span style="float: left">{{ option.label
                                                                                }}</span>
                                                                                <span
                                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                                        option.value }}</span>
                                                                            </el-option>

                                                                        </el-select>
                                                                        <el-button icon="el-icon-delete"
                                                                            @click.prevent="removePermissibleValues(item)"></el-button>
                                                                    </div>
                                                                </div>
                                                            </el-form-item>
                                                        </div>
                                                        <div>
                                                            <el-button type="primary" icon="el-icon-plus"
                                                                @click="addValueDomainItem">添加</el-button>
                                                        </div>
                                                    </el-form-item>


                                                    <el-form-item>
                                                        <el-button type="primary"
                                                            @click="registerValueDomainvalue">添加</el-button>
                                                        <el-button type="danger"
                                                            @click="resetFormMDR('registerValueDomainFormvalue')">重置</el-button>
                                                    </el-form-item>
                                                </el-form>
                                            </div>
                                        </div>

                                        <!-- 新增值含义 -->
                                        <div v-show="showaddConceptualDomain" class="showbox" style="width:33vw">
                                            <div>
                                                <h3 style="margin-bottom: 20px;">概念域添加值含义</h3>
                                            </div>
                                            <div>
                                                <!-- {% raw %} -->
                                                <el-form :model="registerConceptualDomainData"
                                                    ref="registerConceptualDomainForm" label-width="auto"
                                                    class="demo-dynamic" style="width: 90%;"
                                                    v-show="showaddConceptualDomain">

                                                    <el-form-item label="概念域:" prop="conceptualDomain">
                                                        <el-select v-model="registerValueDomainData.conceptualDomain"
                                                            filterable remote @focus="searchConceptualDomain"
                                                            :loading="conceptualDomainLoading" :value-key="'label'">
                                                            <!-- {% raw %} -->
                                                            <el-option v-for="(option, index) in conceptualDomainOptions"
                                                                :key="index" :label="option.label" :value="option.value">
                                                                <span style="float: left">{{ option.label }}</span>
                                                                <span
                                                                    style="float: right; color: #8492a6; font-size: 13px">{{
                                                                        option.value }}</span>
                                                            </el-option>
                                                            <!-- {% endraw %} -->
                                                        </el-select>
                                                    </el-form-item>

                                                    <el-form-item
                                                        v-for="(valueMeaning, index) in registerConceptualDomainData.valueMeanings"
                                                        :label="'值含义:' + (startIndex + index)" :key="startIndex + index"
                                                        prop="'valueMeaning'  + (startIndex + index)">
                                                        <div style="display: flex; align-items: center;">
                                                            <el-input
                                                                v-model="registerConceptualDomainData.valueMeanings[index]"
                                                                width="20px" clearable placeholder="请输入内容"></el-input>
                                                            <el-button icon="el-icon-delete" style="margin-left: 10px;"
                                                                @click.prevent="removeValueMeaning(valueMeaning)"
                                                                circle></el-button>
                                                        </div>
                                                    </el-form-item>
                                                    <el-form-item>
                                                        <el-button type="primary"
                                                            @click="registeraddConceptualDomainvalue">注册</el-button>
                                                        <el-button @click="addValueMeaning"
                                                            icon="el-icon-plus">新增值含义</el-button>
                                                        <el-button type="danger"
                                                            @click="resetFormMDR('registerConceptualDomainForm')">重置</el-button>
                                                    </el-form-item>
                                                </el-form>
                                                <!-- {% endraw %} -->
                                            </div>
                                        </div>
                                    </el-main>
                                </el-col>
                            </el-row>
                        </div>
                        <!-- 子域注册 -->
                        <div v-show="showsubDomain">
                            <el-main>
                                <template>
                                    <el-tabs v-model="activeName">
                                        <!-- 建立表属性与数据元之间联系 -->
                                        <el-tab-pane label="表属性" name="first">
                                            <el-divider content-position="center">表属性名</el-divider>
                                            <div style="margin: 20px;">
                                                <el-input v-model="attributeName" :disabled="true"></el-input>
                                            </div>
                                            <el-divider content-position="center">数据元</el-divider>
                                            <div style="margin: 20px; display: flex;">
                                                <el-select v-model="dataElement" filterable remote :value-key="'label'"
                                                    clearable>
                                                    <!-- {% raw %} -->
                                                    <el-option v-for="option in dataElementOptions" :key="option.value"
                                                        :label="option.label" :value="option.value">
                                                        <span style="float: left">{{ option.label }}</span>
                                                        <span style="float: right; color: #8492a6; font-size: 13px">{{
                                                            option.value }}</span>
                                                    </el-option>
                                                    <!-- {% endraw %} -->
                                                </el-select>
                                            </div>
                                            <div style="margin: 20px; display: flex;">
                                                <el-button type="primary"
                                                    @click="addRelationBetweenAttributeAndDataElement">添加联系</el-button>
                                            </div>
                                        </el-tab-pane>

                                        <!-- 建立表属性与可允许值联系 -->
                                        <el-tab-pane label="表属性值" name="second">
                                            <el-divider content-position="center">表属性值名</el-divider>
                                            <div style="margin: 20px;">
                                                <el-input v-model="attributeValueName" :disabled="true"></el-input>
                                            </div>
                                            <el-divider content-position="center">可允许值</el-divider>
                                            <div class="block">
                                                <!-- <span class="demonstration">请选择:   </span> -->
                                                <el-cascader v-model="permissibleValues" :options="permissibleValuesOptions"
                                                    filterable clearable>
                                                </el-cascader>
                                            </div>
                                            <div style="margin: 20px; display: flex;">
                                                <el-button type="primary"
                                                    @click="addRelationBetweenAttributeValueAndPermissibleValues">添加联系</el-button>
                                            </div>
                                        </el-tab-pane>
                                    </el-tabs>
                                </template>
                            </el-main>
                        </div>
                    </el-card>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import * as echarts from 'echarts';
export default {
    data() {
        return {
            // 滑块value
            value1: true,
            value2: true,
            value3: true,
            value4: true,
            // 图谱展示
            show_subDomain: false,
            show_DataModel: false,
            show_Evolution: false,
            show_MDR: false,
            active: 0,
            // 子域
            options_subDomain: [],
            value_subDomain: [],
            tableModelsubDomain: [],
            graphDatasubDomain: [],
            graphLinkssubDomain: [],
            //子域删除接收
            options_table: [],
            options_tableproperty: [],
            options_tablepropertyValue: [],
            tableModelsubDomain1: {},
            tableModelsubDomain2: {},

            deletetableName: {
                label: '',
                value: '',
            },
            deletetableName1: {
                label: '',
                value: '',
            },
            deletetableName2: {
                label: '',
                value: '',
            },
            deletetablePropertyName: {
                label: '',
                value: '',
            },
            deletetablePropertyValueName: {
                label: '',
                value: '',
            },

            // 信息模型
            optionsOfModelName: [],
            selectedModelName: '',
            graphDatamodel: [],
            graphlinksmodel: [],
            optionsOfModelPropertyName: [],
            // 演化部分
            graphEvolutionData: [],
            graphEvolutionlink: [],
            dialogFormtable: false,
            dialogFormtablevalue: false,
            // formLabelWidth: '120px',
            formtable: {
                name: '',
                identifier: ''
            },
            formtablevalue: {
                name: '',
                identifier: ''
            },
            // MDR
            optionsMDR: [],
            valueMDRname: '',
            graphDataMDR: [],
            graphLinksMDR: [],
            // 对象类修改
            dialogFormclassname: false,
            dialogFormproperty: false,
            dialogFormConceptualDomain: false,
            dialogFormDataElementConcept: false,
            dialogFormValueDomain: false,
            dialogFormDataElement: false,
            formtablevalueMDR: {
                Datavalue: {},
                dataguanlian: {},
                dialogDataValueMenings: [],
            },


            // 三部分的步骤条
            showinformation_model: true,
            showMDRregister: false,
            showsubDomain: false,
            // 步骤条1信息模型演化部分
            addClassName: {
                class_name: ''
            },
            showAddModelClassTable: true,
            showAddModelPropertyTable: false,
            showAddModelRelationTable: false,
            showDeleteModelPropertyTable: false,
            optionsOfModelClassName: [],
            addPropertyName: {
                property_names: [],
                class_name: '',
                model_name: '',
                evolution: 'yes',
                attributeName: '',
                attributeIdentifier: ''
            },
            addRelationData: {
                class_name1: '',
                class_name2: '',
                relation: ''
            },
            deleteProperty: {
                deletePropertyName: [],
            },

            // MDR注册模块
            showObjectClass: true,
            showProperty: false,
            showConceptualDomain: false,
            showDataElementConcept: false,
            showValueDomain: false,
            showDataElement: false,
            showValueDomainValue: false,
            showaddConceptualDomain: false,
            startIndex: 1,
            registerObjectClassData: {
                name: '',
                describe: '',
                personId: '',
                department: ''
            },
            registerPropertyData: {
                name: '',
                describe: '',
                personId: '',
                department: ''
            },
            registerConceptualDomainData: {
                name: '',
                describe: '',
                personId: '',
                department: '',
                valueMeanings: []
            },
            registerDataElementConceptData: {
                name: '',
                describe: '',
                personId: '',
                department: '',
                objectClass: '',
                property: '',
                conceptualDomain: ''
            },
            registerValueDomainData: {
                name: '',
                describe: '',
                personId: '',
                department: '',
                conceptualDomain: '',
                indefinite: '',
                enumerable: []
            },
            registerDataElementData: {
                name: '',
                describe: '',
                personId: '',
                department: '',
                dataElementConcept: '',
                valueDomain: '',
                evolution: "yes",
                attributeName: '',
                attributeIdentifier: ''
            },
            registerValueDomainDataValuelabel: {
                registerValueDomainDataValue: [],
                registerDomainFormValue: '',
            },
            DataDomainOptions: [],

            objectClassOptions: [],
            objectClassLoading: false,
            propertyOptions: [],
            propertyLoading: false,
            conceptualDomainOptions: [],
            conceptualDomainLoading: false,
            valueMeaningsOptions: [],
            valueMeaningsLoading: false,
            dataElementConceptOptions: [],
            dataElementConceptLoading: false,
            valueDomainOptions: [],
            valueDomainLoading: false,
            DataDomainLoading: false,

            // 子域注册模块
            subDomainName: '',
            identifier_table: '',
            // identifier_table_query:'',
            activeName: 'first',
            dataElement: '',
            dataElementOptions: [],
            attributeName: '',
            permissibleValues: [],
            permissibleValuesOptions: [],
            attributeValueName: '',
            EvolutiongraphData: [],
            EvolutiongraphLinks: [],
            selectAttributeName: '',
            selectAttributeIdentifier: ''
        }
    },
    mounted() {
        if (this.$route.query.identifier_table === undefined) {
        } else {
            this.identifier_table = this.$route.query.identifier_table;
            // console.log(this.identifier_table)
            this.searchModelNamesDetails();
        }
        this.searchsubDomaintable();
        this.searchsubDomaintext();
        this.getOptionsOfModelName();
        this.getOptionsOfMDR();
        this.getDataElementOptions();
        this.getValueDomainAndPermissibleValuesOptions();
    },
    methods: {
        // 添加概念域值含义信息
        registeraddConceptualDomainvalue() {
            var vm = this;
            // console.log(this.registerValueDomainData.conceptualDomain)
            // console.log(this.registerConceptualDomainData.valueMeanings)
            this.$axios.post('http://localhost:5000/evolution/mdr/addValueMeanings',
                {
                    params: {
                        identifier_conceptual_domain: this.registerValueDomainData.conceptualDomain,
                        value_meanings: this.registerConceptualDomainData.valueMeanings
                    }
                }
            )
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.resetFormMDR("registerValueDomainFormvalue");
                    vm.getDataElementOptions();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },
                );
        },
        // 获取值域信息
        searchDataDomain() {
            this.DataDomainLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getValueDomainOption')
                .then(response => {
                    this.DataDomainOptions = response.data.data;
                    this.DataDomainLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.DataDomainLoading = false;
                    // 获取失败消息提示
                    // this.$message({
                    //     showClose: true,
                    //     message: "查询失败",
                    //     type: 'error',
                    //     duration: 1000
                    // })
                },

                );
        },
        // 新增属性值
        registerValueDomainvalue() {
            var vm = this;
            // console.log(this.registerValueDomainDataValuelabel.registerDomainFormValue)
            // console.log(this.registerValueDomainData.enumerable)
            this.$axios.post('http://localhost:5000/evolution/mdr/addPermissibleValues',
                {
                    params: {
                        identifier_value_domain: this.registerValueDomainDataValuelabel.registerDomainFormValue,
                        enumerable: this.registerValueDomainData.enumerable
                    }
                }
            )
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.resetFormMDR("registerValueDomainFormvalue");
                    vm.getDataElementOptions();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },
                );
        },
        // 子域方法
        getDataElementOptions() {
            this.$axios.get('http://localhost:5000/search/mdr/getDataElementOption')
                .then(response => {
                    this.dataElementOptions = response.data.data;
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "获取失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        getValueDomainAndPermissibleValuesOptions() {
            // this.valueDomainLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getValueDomainAndPermissibleValuesOption')
                .then(response => {
                    // console.log(response.data.data)
                    this.permissibleValuesOptions = response.data.data;
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "获取失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        // 查询函数
        evolutionsearch() {
            var vm = this;
            // console.log(this.subDomainName)
            // console.log("_______________________________________________________")
            // console.log(this.identifier_table)

            this.$axios.get('http://localhost:5000/search/subDomain/getGraphOfTable', {
                params: {
                    // name: this.searchInput,
                    sub_domain_name: this.subDomainName,
                    identifier_table: this.identifier_table
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.$message.error("查询失败");
                    } else {
                        vm.EvolutiongraphData = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.EvolutiongraphLinks = response.data.links;
                        // console.log(response.data)
                        vm.updateChartOfEvolutiongraph(vm.EvolutiongraphData, vm.EvolutiongraphLinks);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: '查询失败',
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        updateChartOfEvolutiongraph(graphData, graphLinks) {
            var myChart = echarts.init(document.getElementById("GraphEvolution"));
            var vm = this;
            var option = {
                title: {
                    textStyle: {
                        fontWeight: "lighter"
                    }
                },
                // animationDurationUpdate 设置图表更新动画的持续时间
                animationDurationUpdate: 1500,
                // animationEasingUpdate 设置图表更新动画的缓动效果
                animationEasingUpdate: 'quinticInOut',
                legend: {
                    x: "center",
                    show: true,
                    data: ["子域", "表", "表属性", "表属性值", "数据元", "值域", "值域组", "可允许值"]
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 60,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 4],
                    edgeLabel: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 12
                            },
                            formatter: "{c}"
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 100]
                    },
                    focusNodeAdjacency: true,
                    draggable: true,
                    roam: true,
                    categories: [{
                        name: '子域'
                    },
                    {
                        name: '表'
                    },
                    {
                        name: '表属性'
                    },
                    {
                        name: '表属性值'
                    },
                    {
                        name: '数据元'
                    },
                    {
                        name: '值域'
                    },
                    {
                        name: '值域组'
                    },
                    {
                        name: '可允许值'
                    }
                    ],
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 15
                            },
                        }
                    },
                    lineStyle: {
                        normal: {
                            opacity: 0.9,
                            width: 1,
                            curveness: 0.3
                        }
                    },
                    nodes: graphData,
                    links: graphLinks,
                }]
            };
            myChart.setOption(option, true);
        },
        // 添加数据元联系
        addRelationBetweenAttributeAndDataElement() {
            var vm = this;
            // console.log(this.attributeName);
            if (this.attributeName === '') {
                this.$message.error("请先去子域图谱左侧列表选择表属性名");
                return;
            }
            // console.log(this.subDomainName)
            this.$axios.get('http://localhost:5000/register/subDomain/addRelationBetweenAttributeAndDataElement', {
                params: {
                    // sub_domain_name: this.subDomainName,
                    identifier_table: this.identifier_table,
                    name_attribute: this.attributeName,
                    identifier_data_element: this.dataElement
                }
            })
                .then(response => {
                    vm.openSuccessful("添加成功");
                    // vm.searchModelNamesDetails();
                    vm.evolutionsearch();
                })
                .catch(error => {
                    console.error(error);
                },
                );
        },
        // 添加表属性名
        addRelationBetweenAttributeValueAndPermissibleValues() {
            var vm = this;
            // console.log(this.permissibleValues);
            if (this.attributeValueName === '') {
                this.$message.error("请先去子域图谱左侧列表选择表属性值名");
                return;
            }
            this.$axios.get('http://localhost:5000/register/subDomain/addRelationBetweenAttributeValueAndPermissibleValues', {
                params: {
                    sub_domain_name: this.subDomainName,
                    identifier_table: this.identifier_table,
                    name_attribute_value: this.attributeValueName,
                    identifier_permissible_values: this.permissibleValues[1]
                }
            })
                .then(response => {
                    vm.openSuccessful("添加成功");
                    vm.evolutionsearch();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: response.data.message,
                        type: 'error',
                        duration: 1000
                    })
                },
                );
        },
        // MDR一系列方法
        openSuccessful(message) {
            this.$message({
                message: message,
                type: 'success',
                duration: 1000,
                showClose: true,
            });
        },
        //注册对象类 
        registerObjectClass() {
            var vm = this;
            this.$axios.post('http://localhost:5000/register/mdr/objectClass', this.registerObjectClassData)
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    // console.log(this.registerObjectClassData)
                    vm.getDataElementOptions();
                    vm.resetFormMDR("registerObjectClassForm");

                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },
                );
        },
        // 注册属性
        registerProperty() {
            var vm = this;
            this.$axios.post('http://localhost:5000/register/mdr/property', this.registerPropertyData)
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.getDataElementOptions();
                    vm.resetFormMDR("registerPropertyForm");
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        // 注册概念域
        registerConceptualDomain() {
            var vm = this;
            this.$axios.post('http://localhost:5000/register/mdr/conceptualDomain', this.registerConceptualDomainData)
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.getDataElementOptions();
                    vm.resetFormMDR("registerConceptualDomainForm");
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        // 数据元概念注册
        registerDataElementConcept() {
            var vm = this;

            this.$axios.post('http://localhost:5000/register/mdr/dataElementConcept', this.registerDataElementConceptData)
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.getDataElementOptions();
                    vm.resetFormMDR("registerDataElementConceptForm");
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        // 值域注册
        registerValueDomain() {
            var vm = this;
            this.$axios.post('http://localhost:5000/register/mdr/valueDomain', this.registerValueDomainData)
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.getDataElementOptions();
                    vm.resetFormMDR("registerValueDomainForm");
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "注册失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        // 数据元注册
        registerDataElement() {
            var vm = this;
            vm.registerDataElementData.attributeName = vm.selectAttributeName;
            vm.registerDataElementData.attributeIdentifier = vm.selectAttributeIdentifier;
            this.$axios.post('http://localhost:5000/register/mdr/dataElement', this.registerDataElementData)
                .then(response => {
                    let message = response.data.message
                    vm.openSuccessful(message);
                    // console.log(response)
                    vm.getMDRGraph(response.data.identifier_data_element);
                    vm.resetFormMDR("registerDataElementForm");
                    this.searchsubDomaintable();
                    this.searchsubDomaintext();
                    this.getOptionsOfModelName();
                    this.getOptionsOfMDR();
                    this.getDataElementOptions();
                    this.getValueDomainAndPermissibleValuesOptions();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: '注册失败',
                        type: 'error',
                        duration: 1000
                    })
                },
                );
        },

        // 查询对象类
        searchObjectClass(query) {
            this.objectClassLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getObjectClassOptions', {
                params: {
                    query: query
                }
            })
                .then(response => {

                    this.objectClassOptions = response.data.data;
                    this.objectClassLoading = false;
                    // console.log(this.objectClassOptions)
                })
                .catch(error => {
                    console.error(error);
                    this.objectClassLoading = false;
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        searchProperty(query) {
            this.propertyLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getPropertyOption', {
                params: {
                    query: query
                }
            })
                .then(response => {
                    this.propertyOptions = response.data.data;
                    this.propertyLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.propertyLoading = false;
                });
        },
        searchConceptualDomain(query) {
            this.conceptualDomainLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getConceptualDomainOption', {
                params: {
                    query: query
                }
            })
                .then(response => {
                    this.conceptualDomainOptions = response.data.data;
                    this.conceptualDomainLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.conceptualDomainLoading = false;
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        searchValueMeanings(query) {
            this.valueMeaningsLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getValueMeaningsOption', {
                params: {
                    query: query
                }
            })
                .then(response => {
                    this.valueMeaningsOptions = response.data.data;
                    this.valueMeaningsLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.valueMeaningsLoading = false;
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        searchDataElementConcept(query) {
            this.dataElementConceptLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getDataElementConceptOption', {
                params: {
                    query: query
                }
            })
                .then(response => {
                    this.dataElementConceptOptions = response.data.data;
                    this.dataElementConceptLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.dataElementConceptLoading = false;
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        searchValueDomain(query) {
            this.valueDomainLoading = true;
            this.$axios.get('http://localhost:5000/search/mdr/getValueDomainOption', {
                params: {
                    query: query
                }
            })
                .then(response => {
                    this.valueDomainOptions = response.data.data;
                    this.valueDomainLoading = false;
                })
                .catch(error => {
                    console.error(error);
                    this.valueDomainLoading = false;
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "查询失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },

        resetFormMDR(formName) {
            this.$refs[formName].resetFields();
            if (formName == "registerConceptualDomainForm") {
                this.registerConceptualDomainData.valueMeanings = [];
                this.registerValueDomainData.conceptualDomain = '';
            };
            if (formName == "registerValueDomainForm") {
                this.registerValueDomainData.enumerable = [];
            };
            if (formName == "registerValueDomainFormvalue") {
                this.registerValueDomainData.enumerable = [];
                this.registerValueDomainDataValuelabel.registerDomainFormValue = '';
                this.registerValueDomainDataValuelabel.registerValueDomainDataValue = [];
            }
        },

        removeValueMeaning(item) {
            var index = this.registerConceptualDomainData.valueMeanings.indexOf(item);
            if (index !== -1) {
                this.registerConceptualDomainData.valueMeanings.splice(index, 1)
            }
        },
        removePermissibleValues(item) {
            var index = this.registerValueDomainData.enumerable.indexOf(item);
            if (index !== -1) {
                this.registerValueDomainData.enumerable.splice(index, 1);
            };
        },
        addValueMeaning() {
            this.registerConceptualDomainData.valueMeanings.push('')
        },
        addValueDomainItem() {
            this.registerValueDomainData.enumerable.push({
                value: '',
                valueMeaning: '',
                num: ''
            });
        },
        // MDR绑定展示方法
        changeShowObjectClass() {
            this.showObjectClass = true;
            this.showProperty = false;
            this.showConceptualDomain = false;
            this.showDataElementConcept = false;
            this.showValueDomain = false;
            this.showDataElement = false;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = false;
        },
        changeShowProperty() {
            this.showObjectClass = false;
            this.showProperty = true;
            this.showConceptualDomain = false;
            this.showDataElementConcept = false;
            this.showValueDomain = false;
            this.showDataElement = false;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = false;
        },
        changeShowConceptualDomain() {
            this.showObjectClass = false;
            this.showProperty = false;
            this.showConceptualDomain = true;
            this.showDataElementConcept = false;
            this.showValueDomain = false;
            this.showDataElement = false;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = false;
        },
        changeShowDataElementConcept() {
            this.showObjectClass = false;
            this.showProperty = false;
            this.showConceptualDomain = false;
            this.showDataElementConcept = true;
            this.showValueDomain = false;
            this.showDataElement = false;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = false;
        },
        changeShowValueDomain() {
            this.showObjectClass = false;
            this.showProperty = false;
            this.showConceptualDomain = false;
            this.showDataElementConcept = false;
            this.showValueDomain = true;
            this.showDataElement = false;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = false;
        },
        changeShowDataElement() {
            this.showObjectClass = false;
            this.showProperty = false;
            this.showConceptualDomain = false;
            this.showDataElementConcept = false;
            this.showValueDomain = false;
            this.showDataElement = true;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = false;
        },
        changeShowDataValue() {
            this.showObjectClass = false;
            this.showProperty = false;
            this.showConceptualDomain = false;
            this.showDataElementConcept = false;
            this.showValueDomain = false;
            this.showDataElement = false;
            this.showValueDomainValue = true;
            this.showaddConceptualDomain = false;
        },
        changeShowConceptualDomainValue() {
            this.showObjectClass = false;
            this.showProperty = false;
            this.showConceptualDomain = false;
            this.showDataElementConcept = false;
            this.showValueDomain = false;
            this.showDataElement = false;
            this.showValueDomainValue = false;
            this.showaddConceptualDomain = true;
        },
        // 信息模型按钮绑定展示方法
        changeShowAddModelClassTable() {
            this.showAddModelClassTable = true;
            this.showAddModelPropertyTable = false;
            this.showAddModelRelationTable = false;
        },
        changeShowAddModelPropertyTable() {
            this.showAddModelPropertyTable = true;
            this.showAddModelClassTable = false;
            this.showAddModelRelationTable = false;
        },
        changeShowAddModelRelationTable() {
            this.showAddModelRelationTable = true;
            this.showAddModelClassTable = false;
            this.showAddModelPropertyTable = false;
        },
        changeShowDeleteModelPropertyTable() {
            this.showAddModelClassTable = false;
            this.showAddModelPropertyTable = false;
            this.showAddModelRelationTable = false;
            this.showDeleteModelPropertyTable = true;
        },
        removePropertyItem(index) {
            this.addPropertyName.property_names.splice(index, 1);
        },
        addPropertyItem() {
            this.addPropertyName.property_names.push('');
        },
        // 信息模型注册清除
        resetFormModel() {
            this.addPropertyName.property_names = [];
            this.addPropertyName.class_name = '';
            this.addClassName.class_name = '';
            this.addRelationData.class_name1 = '';
            this.addRelationData.class_name2 = '';
            this.addRelationData.relation = '';
            this.deleteProperty.deletePropertyName = [];
        },
        // 查询消息提示
        opennews(message) {
            this.$message({
                showClose: true,
                message: message,
                type: 'success',
                duration: 1000
            });
        },
        // 查询已经注册的类
        getMdodelClassNameOptions() {
            this.$axios.get('http://localhost:5000/search/model/getModelClassNameOptions', {
                params: {
                    model_name: this.selectedModelName,
                }
            })
                .then(response => {
                    this.optionsOfModelClassName = response.data.data;
                })
                .catch(
                    error => {
                        console.error(error);
                        // 获取失败消息提示
                        this.$message({
                            showClose: true,
                            message: "查询失败",
                            type: 'error',
                            duration: 1000
                        })
                    },
                );
        },
        // 注册关系
        addRelation() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            this.$axios.get('http://localhost:5000/register/model/addRelation', {
                params: {
                    model_name: this.selectedModelName,
                    class_name1: this.addRelationData.class_name1,
                    class_name2: this.addRelationData.class_name2,
                    relation: this.addRelationData.relation
                }
            })
                .then(function (response) {
                    vm.opennews(response.data.message);
                    // vm.showDialogOfAddRelation = false;
                    vm.graphDatamodel = [];
                    vm.graphlinksmodel = [];
                    vm.searchModelName()
                    vm.resetFormModel();
                })
                .catch(function (error) {
                    console.log(error);
                },
                );

        },
        // 注册属性函数
        addProperty() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            vm.addPropertyName.model_name = vm.selectedModelName;
            vm.addPropertyName.attributeName = vm.selectAttributeName,
                vm.addPropertyName.attributeIdentifier = vm.selectAttributeIdentifier;
            this.$axios.post('http://localhost:5000/register/model/addProperty', vm.addPropertyName)
                .then(function (response) {
                    vm.opennews(response.data.message);
                    // vm.showDialogOfAddProperty = false;
                    vm.graphDatamodel = [];
                    vm.graphlinksmodel = [];
                    vm.searchModelName()
                    vm.resetFormModel();
                })
                .catch(error => {
                    console.log(error)
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "添加失败",
                        type: 'error',
                        duration: 1000
                    })
                }
                );
        },
        // 注册类函数
        addClass() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            this.$axios.post('http://localhost:5000/register/model/addClass',
                {
                    params: {
                        model_name: this.selectedModelName,
                        class_name: this.addClassName.class_name,
                        evolution: "yes",
                        attributeName: vm.selectAttributeName,
                        attributeIdentifier: vm.selectAttributeIdentifier
                    }
                })
                .then(response => {
                    // 获取成功消息提示
                    vm.$message({
                        showClose: true,
                        message: response.data.message,
                        type: 'success',
                        duration: 1000
                    })
                    // vm.showDialogOfAddClass = false;
                    vm.graphDatamodel = [];
                    vm.graphlinksmodel = [];
                    vm.searchModelName()
                    vm.getMdodelClassNameOptions();
                    vm.resetFormModel();
                })
                .catch(error => {
                    console.log(error);
                    //获取失败消息提示
                    // this.$message({
                    //     showClose: true,
                    //     message: '添加失败，请检查网络设置',
                    //     type: 'error',
                    //     duration: 1000
                    // })
                }
                );
        },
        //查询已注册属性
        getModelPropertyNameOptions() {
            this.$axios.get('http://localhost:5000/search/model/getClassNameAndPropertyNameOptions', {
                params: {
                    model_name: this.selectedModelName,
                }
            })
                .then(response => {
                    // console.log(response.data);
                    this.optionsOfModelPropertyName = response.data;
                })
                .catch(
                    error => {
                        console.error(error);
                        // 获取失败消息提示
                        this.$message({
                            showClose: true,
                            message: "查询失败",
                            type: 'error',
                            duration: 1000
                        })
                    },
                );
        },
        // 属性删除
        DeletePropertyName() {
            var vm = this;
            if (this.selectedModelName === '') {
                this.$message.error("请先选择信息模型");
                return;
            }
            // console.log(this.deletePropertyName)
            this.$axios.post('http://localhost:5000/evolution/model/deletePropertyOfName',
                {
                    params: {
                        model_name: this.selectedModelName,
                        class_name: this.deleteProperty.deletePropertyName[0],
                        property_name: this.deleteProperty.deletePropertyName[1],
                    }
                }
            )
                .then(response => {
                    console.log(response)
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.getModelPropertyNameOptions();
                    vm.resetFormModel();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "删除失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },

        // MDR图谱查询
        getMDRGraph(identifier) {
            var vm = this;
            // vm.dialogVisibleGraph = true;
            this.$axios.get('http://localhost:5000/search/mdr/getGraphOfMDR', {
                params: {
                    identifier: identifier
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.openError();
                    } else {
                        // console.log(response.data.data);
                        vm.graphDataMDR = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.graphLinksMDR = response.data.links;
                        if (vm.show_MDR === false) {
                            vm.$message.error("请先打开图谱展示开关")
                            return;
                        }
                        vm.updateChartOfMDRGraph(vm.graphDataMDR, vm.graphLinksMDR);
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        // MDR图谱
        updateChartOfMDRGraph(graphData, graphLinks) {
            var myChart = echarts.init(document.getElementById("MDRGraph"));
            var vm = this;
            var option = {
                tooltip: {
                    formatter: function (params) {
                        const nodeData = params.data;
                        let tooltipContent = '';

                        // 检查属性是否存在，存在则添加到tooltipContent中
                        function appendIfExists(property, displayName) {
                            if (nodeData[property]) {
                                tooltipContent += `${displayName}：${nodeData[property]}<br/>`;
                            }
                        }

                        appendIfExists('name', '名称');
                        appendIfExists('describe', '描述');
                        appendIfExists('identifier', '标识符');
                        appendIfExists('department', '创建单位');
                        appendIfExists('personId', 'Person ID');
                        appendIfExists('status', '注册状态');
                        appendIfExists('time', '时间');
                        appendIfExists('version', '版本');

                        return tooltipContent;
                    }
                },

                title: {
                    textStyle: {
                        fontWeight: "lighter"
                    }
                },
                // animationDurationUpdate 设置图表更新动画的持续时间
                animationDurationUpdate: 1500,
                // animationEasingUpdate 设置图表更新动画的缓动效果
                animationEasingUpdate: 'quinticInOut',
                legend: {
                    x: "center",
                    show: true,
                    data: ["对象类", "属性", "概念域", "数据元概念", "值域", "数据元", "可允许值", "值含义", "值域组"]
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 60,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 4],
                    edgeLabel: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 12
                            },
                            formatter: "{c}"
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 100]
                    },
                    focusNodeAdjacency: true,
                    draggable: true,
                    roam: true,
                    categories: [{
                        name: '对象类'
                    },
                    {
                        name: '属性'
                    },
                    {
                        name: '概念域'
                    },
                    {
                        name: '数据元概念'
                    },
                    {
                        name: '值域'
                    },
                    {
                        name: '数据元'
                    },
                    {
                        name: '可允许值'
                    },
                    {
                        name: '值含义'
                    },
                    {
                        name: "值域组"
                    }
                    ],
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 15
                            },
                        }
                    },
                    lineStyle: {
                        normal: {
                            opacity: 0.9,
                            width: 1,
                            curveness: 0.3
                        }
                    },
                    nodes: graphData,
                    links: graphLinks,
                }]
            };
            myChart.setOption(option, true);
            myChart.off('click');
            myChart.on("click", function (params) {
                console.log(params);
                if (params.data.category === 0) {
                    vm.dialogFormclassname = true;
                    vm.handleGetMDRTable(params.data.identifier, "对象类")
                } else if (params.data.category === 1) {
                    vm.dialogFormproperty = true;
                    vm.handleGetMDRTable(params.data.identifier, "属性")
                } else if (params.data.category === 2) {
                    vm.dialogFormConceptualDomain = true;
                    vm.handleGetMDRTable(params.data.identifier, "概念域")
                } else if (params.data.category === 3) {
                    vm.dialogFormDataElementConcept = true;
                    vm.handleGetMDRTable(params.data.identifier, "数据元概念")
                } else if (params.data.category === 4) {
                    vm.dialogFormValueDomain = true;
                    vm.handleGetMDRTable(params.data.identifier, "值域")
                } else if (params.data.category === 5) {
                    vm.dialogFormDataElement = true;
                    vm.handleGetMDRTable(params.data.identifier, "数据元")
                }

            });
        },
        handleGetMDRTable(identifier, label) {
            var vm = this;
            // console.log(identifier)
            // console.log(label)
            this.$axios.get('http://localhost:5000/search/mdr/getMDRTable', {
                params: {
                    identifier: identifier,
                    label: label
                }
            })
                .then(function (response) {
                    console.log(response.data.data);

                    if (label == "概念域") {
                        vm.formtablevalueMDR.Datavalue = response.data.data[0][0];
                        vm.formtablevalueMDR.dialogDataValueMenings = response.data.data[1];
                    } else if (label == "数据元概念") {
                        vm.formtablevalueMDR.Datavalue = { ...response.data.data[0] };
                        const excludedProperties = ['CDMIdentifier', 'CDMName', 'OCLIdentifier', 'OCLName', 'PRPIdentifier', 'PRPName'];
                        for (const prop of excludedProperties) {
                            delete vm.formtablevalueMDR.Datavalue[prop];
                        }
                    } else if (label == "值域") {
                        vm.formtablevalueMDR.dialogDataValueMenings = response.data.data[1];
                        vm.formtablevalueMDR.Datavalue = { ...response.data.data[0][0] };
                        const excludedProperties = ['CDMIdentifier', 'CDMName'];
                        // 从 vm.formtablevalueMDR.Datavalue 中删除指定的属性
                        for (const prop of excludedProperties) {
                            delete vm.formtablevalueMDR.Datavalue[prop];
                        }
                    } else if (label == "数据元") {
                        // vm.formtablevalueMDR.dialogDataValueMenings = response.data.data[1];
                        vm.formtablevalueMDR.Datavalue = { ...response.data.data[0] };
                        const excludedProperties = ['DECIdentifier', 'DECName', 'VDMIdentifier', 'VDMName'];
                        // 从 vm.formtablevalueMDR.Datavalue 中删除指定的属性
                        for (const prop of excludedProperties) {
                            delete vm.formtablevalueMDR.Datavalue[prop];
                        }
                    } else {
                        vm.formtablevalueMDR.Datavalue = response.data.data[0];
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        // 修改MDR对象类
        modifyclassname() {
            let vm = this;
            // console.log(vm.formtablevalueMDR.identifier)
            this.$axios.post('http://localhost:5000/evolution/mdr/updateMDR', {
                params: {
                    label: "对象类",
                    identifier: vm.formtablevalueMDR.Datavalue.identifier,
                    properties: vm.formtablevalueMDR.Datavalue,
                }
            })
                .then(response => {
                    vm.dialogFormclassname = false;
                    vm.$message.success("修改成功");
                    vm.getMDRGraph(vm.valueMDRname);
                })
                .catch(error => {
                    vm.dialogFormclassname = false;
                    console.log(error)
                })
        },
        // 修改MDR属性
        modifyproperty() {
            let vm = this;
            this.$axios.post('http://localhost:5000/evolution/mdr/updateMDR', {
                params: {
                    label: "属性",
                    identifier: vm.formtablevalueMDR.Datavalue.identifier,
                    properties: vm.formtablevalueMDR.Datavalue,
                }
            })
                .then(response => {
                    vm.dialogFormproperty = false;
                    vm.$message.success("修改成功");
                    vm.getMDRGraph(vm.valueMDRname);
                })
                .catch(error => {
                    vm.dialogFormproperty = false;
                    console.log(error)
                })
        },
        // 修改MDR概念域
        modifyConceptualDomain() {
            let vm = this;
            this.$axios.post('http://localhost:5000/evolution/mdr/updateMDR', {
                params: {
                    label: "概念域",
                    identifier: vm.formtablevalueMDR.Datavalue.identifier,
                    properties: vm.formtablevalueMDR.Datavalue,
                }
            })
                .then(response => {
                    vm.dialogFormConceptualDomain = false;
                    vm.$message.success("修改成功");
                    vm.getMDRGraph(vm.valueMDRname);
                })
                .catch(error => {
                    vm.dialogFormConceptualDomain = false;
                    console.log(error)
                })
        },
        // 修改数据元概念
        modifyDataElementConcept() {
            let vm = this;
            this.$axios.post('http://localhost:5000/evolution/mdr/updateMDR', {
                params: {
                    label: "数据元概念",
                    identifier: vm.formtablevalueMDR.Datavalue.identifier,
                    properties: vm.formtablevalueMDR.Datavalue,
                }
            })
                .then(response => {
                    vm.dialogFormDataElementConcept = false;
                    vm.$message.success("修改成功");
                    vm.getMDRGraph(vm.valueMDRname);
                })
                .catch(error => {
                    vm.dialogFormDataElementConcept = false;
                    console.log(error)
                })
        },
        // 修改值域
        modifyValueDomain() {
            let vm = this;
            this.$axios.post('http://localhost:5000/evolution/mdr/updateMDR', {
                params: {
                    label: "值域",
                    identifier: vm.formtablevalueMDR.Datavalue.identifier,
                    properties: vm.formtablevalueMDR.Datavalue,
                }
            })
                .then(response => {
                    vm.dialogFormValueDomain = false;
                    vm.$message.success("修改成功");
                    vm.getMDRGraph(vm.valueMDRname);
                })
                .catch(error => {
                    vm.dialogFormValueDomain = false;
                    console.log(error)
                })
        },
        // 数据元修改
        modifyDataElement() {
            let vm = this;
            this.$axios.post('http://localhost:5000/evolution/mdr/updateMDR', {
                params: {
                    label: "数据元",
                    identifier: vm.formtablevalueMDR.Datavalue.identifier,
                    properties: vm.formtablevalueMDR.Datavalue,
                }
            })
                .then(response => {
                    vm.dialogFormDataElement = false;
                    vm.$message.success("修改成功");
                    vm.getMDRGraph(vm.valueMDRname);
                })
                .catch(error => {
                    vm.dialogFormDataElement = false;
                    console.log(error)
                })
        },

        //子域表单清除
        resetForm() {
            this.deletetableName = {};
            this.deletetableName1 = {};
            this.deletetableName2 = {};
            this.tableModelsubDomain1 = {};
            this.deletetablePropertyName = {};
            this.deletetablePropertyValueName = {};
            this.tableModelsubDomain2 = {};
        },
        // 子域修改下拉框
        searchsubDomaintable() {
            this.$axios.get('http://localhost:5000/search/subDomain/getTableOptions')
                .then(response => {
                    // console.log(response)
                    this.options_table = response.data.data
                })
                .catch(
                    error => {
                        console.error(error);
                        // 获取失败消息提示
                        this.$message({
                            showClose: true,
                            message: "查询失败",
                            type: 'error',
                            duration: 1000
                        })
                    },
                );
        },
        //子域表删除
        DeletetableName() {
            var vm = this;
            // console.log(this.deletetableName.value)
            this.$axios.post('http://localhost:5000/evolution/subDomain/deleteTable',
                {
                    params: {
                        identifier_table: this.deletetableName.value,
                    }
                }
            )
                .then(response => {
                    // console.log(this.deletetableName.value)
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.searchsubDomaintable();
                    vm.searchsubDomaintext();
                    vm.resetForm();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "删除失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        //表属性查询
        searchtableProperty() {
            let vm = this;
            // console.log(this.deletetableName1.value)
            this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainProperties', {
                params: {
                    // 表格ID
                    identifier_table: this.deletetableName1.value
                }
            })
                .then(function (response) {
                    // console.log(response.data)
                    vm.tableModelsubDomain1 = response.data;
                    // console.log(vm.tableModelsubDomain1)
                    vm.options_tableproperty = vm.tableModelsubDomain1
                    //     vm.options_tableproperty = vm.tableModelsubDomain1.flatMap(item => {
                    //         return item.children
                    // });
                    //    console.log(vm.options_tableproperty) 
                }
                )
                .catch(function (error) {
                    console.log(error);
                },
                );
        },
        //子域表属性删除
        DeletetablePropertyName() {
            var vm = this;
            // console.log(this.deletetablePropertyName.value)
            this.$axios.post('http://localhost:5000/evolution/subDomain/deleteAttribute',
                {
                    params: {
                        identifier_attribute: this.deletetablePropertyName.value,
                    }
                }
            )
                .then(response => {
                    // console.log(this.deletetableName.value)
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.searchsubDomaintable();
                    vm.searchtableProperty();
                    vm.searchsubDomaintext();
                    vm.resetForm();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "删除失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },
        //表属性值查询
        searchtablePropertyValue() {
            let vm = this;
            // console.log(this.deletetableName2.value)
            this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainExistAttributeValueOptions', {
                params: {
                    // 表格ID
                    identifier_table: this.deletetableName2.value
                }
            })
                .then(function (response) {
                    // console.log(response.data)
                    vm.tableModelsubDomain2 = response.data.data;
                    if (response.data.data.length == 0) {
                        vm.$message.error("该表表属性值为空")
                        return;
                    }
                    vm.options_tablepropertyValue = vm.tableModelsubDomain2.flatMap(item => {
                        return item.children
                    });
                }
                )
                .catch(function (error) {
                    console.log(error);
                },
                );
        },
        //删除子域表属性值
        DeletetablePropertyValueName() {
            var vm = this;
            console.log(this.deletetablePropertyValueName.value)
            this.$axios.post('http://localhost:5000/evolution/subDomain/deleteAttributeValue',
                {
                    params: {
                        identifier_attribute_value: this.deletetablePropertyValueName.value,
                    }
                }
            )
                .then(response => {
                    // console.log(this.deletetableName.value)
                    let message = response.data.message
                    vm.openSuccessful(message);
                    vm.searchsubDomaintable();
                    vm.searchtablePropertyValue();
                    vm.searchsubDomaintext();
                    vm.resetForm();
                })
                .catch(error => {
                    console.error(error);
                    // 获取失败消息提示
                    this.$message({
                        showClose: true,
                        message: "删除失败",
                        type: 'error',
                        duration: 1000
                    })
                },

                );
        },

        // MDR下拉框查询
        getOptionsOfMDR() {
            this.$axios.get('http://localhost:5000/search/mdr/getDataElementOption')
                .then(response => {
                    this.optionsMDR = response.data.data;
                })
                .catch(error => {
                    console.error(error);
                },
                );
        },
        // 信息模型下拉框查询函数
        getOptionsOfModelName() {
            this.$axios.get('http://localhost:5000/search/model/getModelTypeOptions')
                .then(response => {
                    this.optionsOfModelName = response.data.data;
                })
                .catch(error => {
                    console.error(error);
                },
                );
        },
        // 查询失败函数
        openError() {
            this.$message.error('未查询到结果，请检查输入查询内容是否正确！');
        },
        // 信息模型图形函数
        updateChart(graphData, graphLinks) {
            var myChart = echarts.init(document.getElementById("chartIdModel"));
            var option = {
                title: {
                    textStyle: {
                        fontWeight: "lighter"
                    }
                },
                // animationDurationUpdate 设置图表更新动画的持续时间
                animationDurationUpdate: 1500,
                // animationEasingUpdate 设置图表更新动画的缓动效果
                animationEasingUpdate: 'quinticInOut',
                legend: {
                    x: "center",
                    show: true,
                    data: ["模型", "模型类", "模型属性"]
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 60,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 4],
                    edgeLabel: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 12
                            },
                            formatter: "{c}"
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 100]
                    },
                    focusNodeAdjacency: true,
                    draggable: true,
                    roam: true,
                    categories: [{
                        name: '模型'
                    },
                    {
                        name: '模型类'
                    },
                    {
                        name: '模型属性'
                    }
                    ],
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 15
                            },
                        }
                    },
                    lineStyle: {
                        normal: {
                            opacity: 0.9,
                            width: 1,
                            curveness: 0.3
                        }
                    },
                    nodes: graphData,
                    links: graphLinks,
                }]
            };
            myChart.setOption(option, true);
        },
        // 信息模型查询函数
        searchModelName() {
            var vm = this;
            this.$axios.get('http://localhost:5000/search/model/graphOfName', {
                params: {
                    name: this.selectedModelName,
                    label: "模型"
                }
            })
                .then(function (response) {
                    if (response.data.data.length == 0) {
                        vm.openError();
                    } else {
                        vm.getMdodelClassNameOptions();
                        vm.getModelPropertyNameOptions();
                        vm.graphDatamodel = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        vm.graphlinksmodel = response.data.links;
                        if (vm.show_DataModel === false) {
                            vm.$message.error("请先打开图谱展示按钮")
                            return;
                        }
                        vm.updateChart(vm.graphDatamodel, vm.graphlinksmodel);
                        // vm.tableData = response.data.tableData;
                        // vm.showTable = true;
                        vm.descriptionsData = response.data.list;
                        vm.showDescriptions = true;
                    }

                })
                .catch(function (error) {
                    console.log(error);
                    // 获取失败消息提示
                    // this.$message({
                    //     showClose: true,
                    //     message: "查询失败",
                    //     type: 'error',
                    //     duration: 1000
                    // })
                },

                );
        },
        // 开关清除函数
        changeclear(value) {
            // console.log(value)
            let graphData = [];
            let graphLinks = [];

            switch (value) {
                case "opensubDomain":
                    this.show_subDomain = true;
                    this.updatesubDomainGraph(this.graphDatasubDomain, this.graphLinkssubDomain);
                    break;
                case "offsubDomain":
                    this.show_subDomain = false;
                    this.updatesubDomainGraph(graphData, graphLinks);
                    break;
                case "openModelName":
                    this.show_DataModel = true;
                    this.updateChart(this.graphDatamodel, this.graphLinks);
                    break;
                case "offModelName":
                    this.show_DataModel = false;
                    this.updateChart(graphData, graphLinks);
                    break;
                case "openEvolution":
                    this.show_Evolution = true;
                    this.updateEvolutionGraph(this.graphEvolutionData, this.graphEvolutionlink);
                    this.updateChartOfEvolutiongraph(this.EvolutiongraphData, this.EvolutiongraphLinks);
                    break;
                case "offEvolution":
                    this.show_Evolution = false;
                    this.updateEvolutionGraph(graphData, graphLinks);
                    this.updateChartOfEvolutiongraph(graphData, graphLinks);
                    break;
                case "openMDR":
                    this.show_MDR = true;
                    this.updateChartOfMDRGraph(this.graphDataMDR, this.graphLinksMDR);
                    break;
                case "offMDR":
                    this.show_MDR = false;
                    this.updateChartOfMDRGraph(graphData, graphLinks);
                    break;
                default:
                    this.show_subDomain = false;
                    this.show_DataModel = false;
                    this.show_Evolution = false;
                    this.show_MDR = false;
                    this.updatesubDomainGraph(graphData, graphLinks);
                    this.updateChart(graphData, graphLinks);
                    this.updateEvolutionGraph(graphData, graphLinks);
                    this.updateChartOfEvolutiongraph(graphData, graphLinks);
                    this.updateChartOfMDRGraph(graphData, graphLinks);
                    break;
            }
        },
        // 步骤
        front() {
            this.active--;
            if (this.active < 0) {
                this.$message.error("已经到第一步了")
                this.active = 0;
            }
            if (this.active === 0) {
                this.showinformation_model = true;
                this.showMDRregister = false;
                this.showsubDomain = false;
            }
            if (this.active === 1) {
                this.showinformation_model = false;
                this.showMDRregister = true;
                this.showsubDomain = false;
            }
            this.searchsubDomaintable();
            this.searchsubDomaintext();
            this.getOptionsOfModelName();
            this.getOptionsOfMDR();
            this.getDataElementOptions();
            this.getValueDomainAndPermissibleValuesOptions();
        },
        next() {
            // if (this.active++ > 2) this.active = 0;
            this.active++;
            if (this.active > 3) {
                this.$message.error("已经到最后一步了")
                this.active = 3;
            }
            if (this.active === 1) {
                this.showinformation_model = false;
                this.showMDRregister = true;
                this.showsubDomain = false;
            }
            if (this.active === 2) {
                this.showinformation_model = false;
                this.showMDRregister = false;
                this.showsubDomain = true;
            }
            this.searchsubDomaintable();
            this.searchsubDomaintext();
            this.getOptionsOfModelName();
            this.getOptionsOfMDR();
            this.getDataElementOptions();
            this.getValueDomainAndPermissibleValuesOptions();
        },
        // 子域表的下拉框
        searchsubDomaintext() {
            this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainAndTableOptions')
                .then(response => {
                    // console.log(response.data)
                    this.options_subDomain = response.data.data;
                    // console.log(this.options_subDomain)
                    // if(response.data[0].children == undefined){
                    //     vm.$message.error("该表表属性值为空")
                    //     return;
                    // }
                    // this.options_table = this.options_subDomain.flatMap(item => {
                    //     return item.children
                    // });
                })
                .catch(
                    error => {
                        console.error(error);
                        // 获取失败消息提示
                        this.$message({
                            showClose: true,
                            message: "查询失败",
                            type: 'error',
                            duration: 1000
                        })
                    },
                );
        },
        // 子域图形的回调函数
        updatesubDomainGraph(graphData, graphLinks) {
            var myChart = echarts.init(document.getElementById("GraphsubDomain"));
            var vm = this;
            var option = {
                title: {
                    textStyle: {
                        fontWeight: "lighter"
                    }
                },
                // animationDurationUpdate 设置图表更新动画的持续时间
                animationDurationUpdate: 1500,
                // animationEasingUpdate 设置图表更新动画的缓动效果
                animationEasingUpdate: 'quinticInOut',
                legend: {
                    x: "center",
                    show: true,
                    data: ['表属性', '表属性值', '数据元', '值域', '值域组', '可允许值', '值含义']
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 60,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 4],
                    edgeLabel: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 12
                            },
                            formatter: "{c}"
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 100]
                    },
                    focusNodeAdjacency: true,
                    draggable: true,
                    roam: true,
                    categories: [
                        {
                            name: '表属性'
                        },
                        {
                            name: '表属性值'
                        },
                        {
                            name: '数据元'
                        },
                        {
                            name: '值域'
                        },
                        {
                            name: '值域组'
                        },
                        {
                            name: '可允许值'
                        },
                        {
                            name: '值含义'
                        }
                    ],
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 15
                            },
                        }
                    },
                    lineStyle: {
                        normal: {
                            opacity: 0.9,
                            width: 1,
                            curveness: 0.3
                        }
                    },
                    nodes: graphData,
                    links: graphLinks,
                }]
            };
            myChart.setOption(option, true);
            myChart.off('click');
            myChart.on("click", function (params) {
                // console.log(params)
                if (vm.show_Evolution === false) {
                    vm.$message.error("请先打开演化图谱展示按钮")
                    vm.attributeName = params.data.name;
                    return;
                }
                if (params.data.category != 0) {
                    vm.$message.error("请点击表属性节点来查看演化图谱")
                    vm.attributeValueName = params.data.name;
                } else {
                    vm.graphEvolutionData = vm.graphDatasubDomain;
                    vm.graphEvolutionlink = vm.graphLinkssubDomain;
                    vm.updateEvolutionGraph(vm.graphEvolutionData, vm.graphEvolutionlink);
                };
            });
        },
        // 子域左侧列表回调函数
        handleNodeClick(data) {
            let vm = this;
            const table_name = data.label;
            // console.log(data)
            const name = data.label;
            vm.formtable.identifier = data.value
            vm.selectAttributeName = data.label;
            vm.selectAttributeIdentifier = data.value;
            // if(data.children == undefined){
            //     this.$message.error("请选择表属性来展示图谱")
            //     this.attributeValueName = name;
            //     return;
            // }
            this.$axios.get('http://localhost:5000/search/subDomain/getGraphOfAttribute', {
                params: {
                    identifier_attribute: data.value
                }
            })
                .then(response => {
                    // console.log(response)
                    if (response.data.data.length == 0) {
                        return;
                    } else {
                        this.attributeName = table_name;
                        this.graphDatasubDomain = response.data.data.map(function (node, idx) {
                            node.id = idx;
                            return node;
                        });
                        // this.graphDatasubDomain = response.data.data;
                        this.graphLinkssubDomain = response.data.links;
                        if (vm.show_subDomain === false) {
                            vm.$message.error("请先打开图谱展示开关")
                            return;
                        }
                        this.updatesubDomainGraph(this.graphDatasubDomain, this.graphLinkssubDomain);
                        vm.graphEvolutionData = vm.graphDatasubDomain;
                        vm.graphEvolutionlink = vm.graphLinkssubDomain;
                        this.updateEvolutionGraph(this.graphDatasubDomain, this.graphLinkssubDomain);
                    }
                })
                .catch(error => {
                    console.log(error)
                })
        },
        // 子域下拉框调用的函数
        searchModelNamesDetails() {
            let vm = this;
            // console.log(this.value_subDomain);
            // console.log(this.identifier_table);
            if (this.value_subDomain && this.value_subDomain.length > 0) {
                this.subDomainName = this.value_subDomain[0];
                this.identifier_table = this.value_subDomain[1];
            }
            this.$axios.get('http://localhost:5000/search/subDomain/getSubDomainProperties', {
                params: {
                    // 表格ID
                    identifier_table: this.identifier_table
                }
            })
                .then(function (response) {
                    vm.$message.success("查询成功")
                    vm.tableModelsubDomain = response.data;
                    // console.log(response.data)
                }
                )
                .catch(function (error) {
                    console.log(error);
                },
                );
        },
        // 演化图形调用函数
        updateEvolutionGraph(graphData, graphLinks) {
            let vm = this;
            let myChart1 = document.getElementById("GraphEvolution")
            myChart1?.removeAttribute("_echarts_instance_");
            let myChart = echarts.init(myChart1);

            // var vm = this;
            var option = {
                title: {
                    textStyle: {
                        fontWeight: "lighter"
                    }
                },
                // animationDurationUpdate 设置图表更新动画的持续时间
                animationDurationUpdate: 1500,
                // animationEasingUpdate 设置图表更新动画的缓动效果
                animationEasingUpdate: 'quinticInOut',
                legend: {
                    x: "center",
                    show: true,
                    data: ['表属性', '表属性值', '数据元', '值域', '值域组', '可允许值', '值含义']
                },
                series: [{
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 60,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 4],
                    edgeLabel: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 12
                            },
                            formatter: "{c}"
                        }
                    },
                    force: {
                        repulsion: 2500,
                        edgeLength: [10, 100]
                    },
                    focusNodeAdjacency: true,
                    draggable: true,
                    roam: true,
                    categories: [
                        {
                            name: '表属性'
                        },
                        {
                            name: '表属性值'
                        },
                        {
                            name: '数据元'
                        },
                        {
                            name: '值域'
                        },
                        {
                            name: '值域组'
                        },
                        {
                            name: '可允许值'
                        },
                        {
                            name: '值含义'
                        }
                    ],
                    label: {
                        normal: {
                            show: true,
                            textStyle: {
                                fontSize: 15
                            },
                        }
                    },
                    lineStyle: {
                        normal: {
                            opacity: 0.9,
                            width: 1,
                            curveness: 0.3
                        }
                    },
                    nodes: graphData,
                    links: graphLinks,
                }]
            };
            myChart.setOption(option, true);
            myChart.off('click');
            myChart.on("click", function (params) {
                // console.log(params);
                if (params.data.category === 0) {
                    vm.dialogFormtable = true;
                    vm.formtable.identifier = params.data.identifier
                } else if (params.data.category === 1) {
                    vm.dialogFormtablevalue = true;
                    vm.formtablevalue.identifier = params.data.identifier
                } else {
                    vm.$message.error("请选择表属性或表属性值节点进行修改")
                }
            });
        },
        modifytable() {
            let vm = this;
            const id = vm.formtable.identifier;
            // console.log(id)
            vm.$axios.get('http://localhost:5000/evolution/subDomain/updateSubDomain', {
                params: {
                    label: "表属性",
                    identifier: vm.formtable.identifier,
                    name: vm.formtable.name,
                }
            })
                .then(response => {
                    console.log(response)
                    vm.$message.success("修改成功")
                    vm.dialogFormtable = false;
                    vm.searchModelNamesDetails();
                    // 遍历数组中的对象
                    let data = null;
                    for (let i = 0; i < vm.tableModelsubDomain.length; i++) {
                        if (vm.tableModelsubDomain[i].value === id) {
                            data = vm.tableModelsubDomain[i];
                            break;
                        }
                    }
                    vm.handleNodeClick(data);
                    // vm.updateEvolutionGraph(vm.graphEvolutionData,vm.graphEvolutionlink);
                })
                .catch(error => {
                    console.log(error);
                    vm.dialogFormtable = false;
                })
        },
        modifytablevalue() {
            let vm = this;
            // console.log(vm.formtable)
            const id = vm.formtable.identifier;
            // console.log(id)
            vm.$axios.get('http://localhost:5000/evolution/subDomain/updateSubDomain', {
                params: {
                    label: "表属性值",
                    identifier: vm.formtablevalue.identifier,
                    name: vm.formtablevalue.name,
                }
            })
                .then(response => {
                    // console.log(response)
                    vm.$message.success("修改成功")
                    vm.dialogFormtablevalue = false;
                    vm.searchModelNamesDetails();
                    // 遍历数组中的对象
                    let data = null;
                    for (let i = 0; i < vm.tableModelsubDomain.length; i++) {
                        if (vm.tableModelsubDomain[i].value === id) {
                            data = vm.tableModelsubDomain[i];
                            break;
                        }
                    }
                    vm.handleNodeClick(data);
                    // vm.updateEvolutionGraph(vm.graphEvolutionData,vm.graphEvolutionlink);
                })
                .catch(error => {
                    console.log(error)
                    vm.dialogFormtablevalue = false;
                })
        }
    }
}
</script>

<style scoped>
.chartGraph {
    width: 100%;
    height: 540px;
}

.box-contain {
    display: flex;
    margin-left: 250px;
}

.box {
    flex: 1;

}

#box1 {

    margin-right: 0;

}

/* #chartIdModelGraph {
    width: 100%;
    height: calc(50vh - 20px);
    
} 

#chartIdModelData {
  width: 100%;
  height: calc(50vh - 20px);
} */
.button {
    margin-bottom: 10px;
    margin-top: 10px;
    width: 150px;
}

.el-row {
    margin-bottom: 2px;
}

/* .buttom{

} */
</style>
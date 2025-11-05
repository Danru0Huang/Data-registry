
<template>
  <div class="box">
    <el-container>
      <el-main>
        <el-card class="box-card">
          <div slot="header" class="clearfix input-container" style="text-align: center">
            <!-- 选择要查询的类别 -->
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                请选择<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="对象类">对象类</el-dropdown-item>
                <el-dropdown-item command="属性">属性</el-dropdown-item>
                <el-dropdown-item command="概念域">概念域</el-dropdown-item>
                <el-dropdown-item command="数据元概念">数据元概念</el-dropdown-item>
                <el-dropdown-item command="值域">值域</el-dropdown-item>
                <el-dropdown-item command="数据元">数据元</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
          <el-row :gutter="5">
            <!-- 对象类表格列表 -->
            <!-- {% raw %} -->
            <template>
              <el-table :data="tableDataOfObjectClass.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
                " style="width: 100%" v-show="showTableOfObjectClass">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item :label="tableTitle">
                        <span>{{ props.row.name }}</span>
                      </el-form-item>
                      <el-form-item label="标识符">
                        <span>{{ props.row.identifier }}</span>
                      </el-form-item>
                      <el-form-item label="描述">
                        <span>{{ props.row.describe }}</span>
                      </el-form-item>
                      <el-form-item label="注册状态">
                        <span>{{ props.row.status }}</span>
                      </el-form-item>
                      <el-form-item label="创建时间">
                        <span>{{ props.row.time }}</span>
                      </el-form-item>
                      <el-form-item label="版本">
                        <span>{{ props.row.version }}</span>
                      </el-form-item>
                      <el-form-item label="创建人员ID">
                        <span>{{ props.row.personId }}</span>
                      </el-form-item>
                      <el-form-item label="创建单位">
                        <span>{{ props.row.department }}</span>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column label="标识符" prop="identifier">
                </el-table-column>
                <el-table-column :label="tableTitle" prop="name">
                </el-table-column>
                <el-table-column label="描述" prop="describe">
                </el-table-column>
                <el-table-column align="right">
                  <!-- eslint-disable -->
                  <template slot="header" slot-scope="scope">
                    <el-input placeholder="请输入内容" v-model="search" clearable size="mini">
                    </el-input>
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete"
                      @click="handleDelete(scope.$index, scope.row)"></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
            <!-- {% endraw %} -->

            <!-- 属性表格列表 -->
            <!-- {% raw %} -->
            <template>
              <el-table :data="tableDataOfMDRProperty.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
                " style="width: 100%" v-show="showTableOfMDRProperty">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item :label="tableTitle">
                        <span>{{ props.row.name }}</span>
                      </el-form-item>
                      <el-form-item label="标识符">
                        <span>{{ props.row.identifier }}</span>
                      </el-form-item>
                      <el-form-item label="描述">
                        <span>{{ props.row.describe }}</span>
                      </el-form-item>
                      <el-form-item label="注册状态">
                        <span>{{ props.row.status }}</span>
                      </el-form-item>
                      <el-form-item label="创建时间">
                        <span>{{ props.row.time }}</span>
                      </el-form-item>
                      <el-form-item label="版本">
                        <span>{{ props.row.version }}</span>
                      </el-form-item>
                      <el-form-item label="创建人员ID">
                        <span>{{ props.row.personId }}</span>
                      </el-form-item>
                      <el-form-item label="创建单位">
                        <span>{{ props.row.department }}</span>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column label="标识符" prop="identifier">
                </el-table-column>
                <el-table-column :label="tableTitle" prop="name">
                </el-table-column>
                <el-table-column label="描述" prop="describe">
                </el-table-column>
                <el-table-column align="right">
                  <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete"
                      @click="handleDelete(scope.$index, scope.row)"></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
            <!-- {% endraw %} -->

            <!-- 概念域表格列表 -->
            <!-- {% raw %} -->
            <template>
              <el-table :data="tableDataOfConceptualDomain.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
                " style="width: 100%" v-show="showTableOfConceptualDomain">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item :label="tableTitle">
                        <span>{{ props.row.name }}</span>
                      </el-form-item>
                      <!-- <el-divider content-position="center">公共属性</el-divider> -->
                      <el-form-item label="标识符">
                        <span>{{ props.row.identifier }}</span>
                      </el-form-item>
                      <el-form-item label="描述">
                        <span>{{ props.row.describe }}</span>
                      </el-form-item>
                      <el-form-item label="注册状态">
                        <span>{{ props.row.status }}</span>
                      </el-form-item>
                      <el-form-item label="创建时间">
                        <span>{{ props.row.time }}</span>
                      </el-form-item>
                      <!-- <el-divider content-position="center">管理信息</el-divider> -->
                      <el-form-item label="版本">
                        <span>{{ props.row.version }}</span>
                      </el-form-item>
                      <el-form-item label="创建人员ID">
                        <span>{{ props.row.personId }}</span>
                      </el-form-item>
                      <el-form-item label="创建单位">
                        <span>{{ props.row.department }}</span>
                      </el-form-item>
                      <el-divider content-position="center">可枚举值含义</el-divider>
                      <el-form-item v-for="(item, index) in props.row.valueMeanings
                            .valueMeanings" :key="index">
                        <el-descriptions border>
                          <el-descriptions-item label="值含义">{{
                            item.vName
                          }}</el-descriptions-item>
                          <el-descriptions-item label="标识符">{{
                            item.vIdentifier
                          }}</el-descriptions-item>
                          <el-descriptions-item label="注册状态">{{
                            item.vStatus
                          }}</el-descriptions-item>
                          <el-descriptions-item label="创建时间">{{
                            item.vTime
                          }}</el-descriptions-item>
                          <el-descriptions-item label="版本">{{
                            item.vVersion
                          }}</el-descriptions-item>
                        </el-descriptions>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column label="标识符" prop="identifier">
                </el-table-column>
                <el-table-column :label="tableTitle" prop="name">
                </el-table-column>
                <el-table-column label="描述" prop="describe">
                </el-table-column>
                <el-table-column align="right">
                  <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete"
                      @click="handleDelete(scope.$index, scope.row)"></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
            <!-- {% endraw %} -->

            <!-- 数据元概念表格列表 -->
            <!-- {% raw %} -->
            <template>
              <el-table :data="tableDataOfDataElementConcept.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
                " style="width: 100%" v-show="showTableDataElementConcept">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item :label="tableTitle">
                        <span>{{ props.row.name }}</span>
                      </el-form-item>
                      <el-form-item label="标识符">
                        <span>{{ props.row.identifier }}</span>
                      </el-form-item>
                      <el-form-item label="描述">
                        <span>{{ props.row.describe }}</span>
                      </el-form-item>
                      <el-form-item label="注册状态">
                        <span>{{ props.row.status }}</span>
                      </el-form-item>
                      <el-form-item label="创建时间">
                        <span>{{ props.row.time }}</span>
                      </el-form-item>
                      <el-form-item label="版本">
                        <span>{{ props.row.version }}</span>
                      </el-form-item>
                      <el-form-item label="创建人员ID">
                        <span>{{ props.row.personId }}</span>
                      </el-form-item>
                      <el-form-item label="创建单位">
                        <span>{{ props.row.department }}</span>
                      </el-form-item>
                      <el-form-item label="对象类">
                        <span>{{ props.row.OCLName }}</span>
                        <i class="el-icon-right"></i>
                        <span>{{ props.row.OCLIdentifier }}</span>
                        <span><el-link @click="
                          handleGetMDRTable(
                            props.row.OCLIdentifier,
                            '对象类'
                          )
                          "><i class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                      <el-form-item label="属性">
                        <span>{{ props.row.PRPName }}</span>
                        <i class="el-icon-right"></i>
                        <span>{{ props.row.PRPIdentifier }}</span>
                        <span><el-link @click="
                          handleGetMDRTable(props.row.PRPIdentifier, '属性')
                          "><i class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                      <el-form-item label="概念域">
                        <span>{{ props.row.CDMName }}</span>
                        <i class="el-icon-right"></i>
                        <span>{{ props.row.CDMIdentifier }}</span>
                        <span><el-link @click="
                          handleGetMDRTable(
                            props.row.CDMIdentifier,
                            '概念域'
                          )
                          "><i class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column label="标识符" prop="identifier">
                </el-table-column>
                <el-table-column :label="tableTitle" prop="name">
                </el-table-column>
                <el-table-column label="描述" prop="describe">
                </el-table-column>
                <el-table-column align="right">
                  <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete"
                      @click="handleDelete(scope.$index, scope.row)"></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
            <!-- {% endraw %} -->

            <!-- 值域表格列表 -->
            <!-- {% raw %} -->
            <template>
              <el-table :data="tableDataOfValueDomain.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
                " style="width: 100%" v-show="showTableOfValueDomain">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item :label="tableTitle">
                        <span>{{ props.row.name }}</span>
                      </el-form-item>
                      <!-- <el-divider content-position="center">公共属性</el-divider> -->
                      <el-form-item label="标识符">
                        <span>{{ props.row.identifier }}</span>
                      </el-form-item>
                      <el-form-item label="描述">
                        <span>{{ props.row.describe }}</span>
                      </el-form-item>
                      <el-form-item label="注册状态">
                        <span>{{ props.row.status }}</span>
                      </el-form-item>
                      <el-form-item label="创建时间">
                        <span>{{ props.row.time }}</span>
                      </el-form-item>
                      <!-- <el-divider content-position="center">管理信息</el-divider> -->
                      <el-form-item label="版本">
                        <span>{{ props.row.version }}</span>
                      </el-form-item>
                      <el-form-item label="创建人员ID">
                        <span>{{ props.row.personId }}</span>
                      </el-form-item>
                      <el-form-item label="创建单位">
                        <span>{{ props.row.department }}</span>
                      </el-form-item>
                      <el-form-item label="取值规则" v-if="props.row.indefinite">
                        <span>{{ props.row.indefinite }}</span>
                      </el-form-item>
                      <el-form-item label="概念域">
                        <span>{{ props.row.CDMName }}</span>
                        <i class="el-icon-right"></i>
                        <span>{{ props.row.CDMIdentifier }}</span>
                        <span><el-link @click="
                          handleGetMDRTable(
                            props.row.CDMIdentifier,
                            '概念域'
                          )
                          "><i class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                      <el-divider content-position="center">可允许值</el-divider>
                      <el-form-item v-for="(item, index) in props.row.permissibleValues
                            .permissibleValues" :key="index">
                        <el-descriptions :column="2" border>
                          <el-descriptions-item label="值">{{
                            item.PEVName
                          }}</el-descriptions-item>
                          <el-descriptions-item label="标识符">{{
                            item.PEVIdentifier
                          }}</el-descriptions-item>
                          <el-descriptions-item label="值含义">{{
                            item.VLMName
                          }}</el-descriptions-item>
                          <el-descriptions-item label="标识符">{{
                            item.VLMIdentifier
                          }}</el-descriptions-item>
                        </el-descriptions>
                        <el-divider><i class="el-icon-crop"></i></el-divider>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column label="标识符" prop="identifier">
                </el-table-column>
                <el-table-column :label="tableTitle" prop="name">
                </el-table-column>
                <el-table-column label="描述" prop="describe">
                </el-table-column>
                <el-table-column align="right">
                  <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete"
                      @click="handleDelete(scope.$index, scope.row)"></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
            <!-- {% endraw %} -->

            <!-- 数据元表格列表 -->
            <!-- {% raw %} -->
            <template>
              <el-table :data="tableDataOfDataElement.filter(
                (data) =>
                  !search ||
                  data.name.toLowerCase().includes(search.toLowerCase())
              )
                " style="width: 100%" v-show="showTableOfDataElement">
                <el-table-column type="expand">
                  <template slot-scope="props">
                    <el-form label-position="left" inline class="demo-table-expand">
                      <el-form-item :label="tableTitle">
                        <span>{{ props.row.name }}</span>
                      </el-form-item>
                      <el-form-item label="标识符">
                        <span>{{ props.row.identifier }}</span>
                        <span><el-link @click="getMDRGraph(props.row.identifier)"><i
                              class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                      <el-form-item label="描述">
                        <span>{{ props.row.describe }}</span>
                      </el-form-item>
                      <el-form-item label="注册状态">
                        <span>{{ props.row.status }}</span>
                      </el-form-item>
                      <el-form-item label="创建时间">
                        <span>{{ props.row.time }}</span>
                      </el-form-item>
                      <el-form-item label="版本">
                        <span>{{ props.row.version }}</span>
                      </el-form-item>
                      <el-form-item label="创建人员ID">
                        <span>{{ props.row.personId }}</span>
                      </el-form-item>
                      <el-form-item label="创建单位">
                        <span>{{ props.row.department }}</span>
                      </el-form-item>
                      <el-form-item label="数据元概念">
                        <span>{{ props.row.DECName }}</span>
                        <i class="el-icon-right"></i>
                        <span>{{ props.row.DECIdentifier }}</span>
                        <span><el-link @click="
                          handleGetMDRTable(
                            props.row.DECIdentifier,
                            '数据元概念'
                          )
                          "><i class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                      <el-form-item label="值域">
                        <span>{{ props.row.VDMName }}</span>
                        <i class="el-icon-right"></i>
                        <span>{{ props.row.VDMIdentifier }}</span>
                        <span><el-link @click="
                          handleGetMDRTable(props.row.VDMIdentifier, '值域')
                          "><i class="el-icon-view el-icon--right"></i> </el-link></span>
                      </el-form-item>
                    </el-form>
                  </template>
                </el-table-column>
                <el-table-column label="标识符" prop="identifier">
                </el-table-column>
                <el-table-column :label="tableTitle" prop="name">
                </el-table-column>
                <el-table-column label="描述" prop="describe">
                </el-table-column>
                <el-table-column align="right">
                  <template slot="header" slot-scope="scope">
                    <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
                  </template>
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete"
                      @click="handleDelete(scope.$index, scope.row)"></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
            <!-- {% endraw %} -->
          </el-row>

          <!-- 当点击表格中对象类的按钮时弹出该弹框,展示该对象类的信息 -->
          <!-- {% raw %} -->
          <el-dialog :visible.sync="dialogVisibleObjectClass" title="对象类" width="50%">
            <el-descriptions border>
              <el-descriptions-item label="对象类">{{
                dialogDataObjectClass.name
              }}</el-descriptions-item>
              <el-descriptions-item label="标识符">{{
                dialogDataObjectClass.identifier
              }}</el-descriptions-item>
              <el-descriptions-item label="描述">{{
                dialogDataObjectClass.describe
              }}</el-descriptions-item>
              <el-descriptions-item label="注册状态">{{
                dialogDataObjectClass.status
              }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{
                dialogDataObjectClass.time
              }}</el-descriptions-item>
              <el-descriptions-item label="版本">{{
                dialogDataObjectClass.version
              }}</el-descriptions-item>
              <el-descriptions-item label="创建人员ID">{{
                dialogDataObjectClass.personId
              }}</el-descriptions-item>
              <el-descriptions-item label="创建单位">{{
                dialogDataObjectClass.department
              }}</el-descriptions-item>
            </el-descriptions>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisibleObjectClass = false">关闭</el-button>
            </span>
          </el-dialog>

          <!-- 当点击表格中的属性按钮时,弹出该弹框.展示属性信息 -->
          <el-dialog :visible.sync="dialogVisibleProperty" title="属性" width="50%">
            <el-descriptions border>
              <el-descriptions-item label="属性">{{
                dialogDataProperty.name
              }}</el-descriptions-item>
              <el-descriptions-item label="标识符">{{
                dialogDataProperty.identifier
              }}</el-descriptions-item>
              <el-descriptions-item label="描述">{{
                dialogDataProperty.describe
              }}</el-descriptions-item>
              <el-descriptions-item label="注册状态">{{
                dialogDataProperty.status
              }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{
                dialogDataProperty.time
              }}</el-descriptions-item>
              <el-descriptions-item label="版本">{{
                dialogDataProperty.version
              }}</el-descriptions-item>
              <el-descriptions-item label="创建人员ID">{{
                dialogDataProperty.personId
              }}</el-descriptions-item>
              <el-descriptions-item label="创建单位">{{
                dialogDataProperty.department
              }}</el-descriptions-item>
            </el-descriptions>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisibleProperty = false">关闭</el-button>
            </span>
          </el-dialog>

          <!-- 当点击表格中的概念域按钮时弹出该弹框,展示概念域信息 -->
          <el-dialog :visible.sync="dialogVisibleConceptualDomain" title="概念域" width="50%">
            <el-descriptions border>
              <el-descriptions-item label="概念域">{{
                dialogDataConceptualDomain.name
              }}</el-descriptions-item>
              <el-descriptions-item label="标识符">{{
                dialogDataConceptualDomain.identifier
              }}</el-descriptions-item>
              <el-descriptions-item label="描述">{{
                dialogDataConceptualDomain.describe
              }}</el-descriptions-item>
              <el-descriptions-item label="注册状态">{{
                dialogDataConceptualDomain.status
              }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{
                dialogDataConceptualDomain.time
              }}</el-descriptions-item>
              <el-descriptions-item label="版本">{{
                dialogDataConceptualDomain.version
              }}</el-descriptions-item>
              <el-descriptions-item label="创建人员ID">{{
                dialogDataConceptualDomain.personId
              }}</el-descriptions-item>
              <el-descriptions-item label="创建单位">{{
                dialogDataConceptualDomain.department
              }}</el-descriptions-item>
            </el-descriptions>
            <el-divider content-position="center">值含义信息</el-divider>
            <div v-if="dialogDataValueMenings">
              <el-descriptions v-for="(item, index) in dialogDataValueMenings" border style="margin-bottom: 20px"
                :key="index">
                <el-descriptions-item label="值含义">{{
                  item.name
                }}</el-descriptions-item>
                <el-descriptions-item label="标识符">{{
                  item.identifier
                }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">{{
                  item.time
                }}</el-descriptions-item>
                <el-descriptions-item label="注册状态">{{
                  item.status
                }}</el-descriptions-item>
                <el-descriptions-item label="版本">{{
                  item.version
                }}</el-descriptions-item>
              </el-descriptions>
            </div>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisibleConceptualDomain = false">关闭</el-button>
            </span>
          </el-dialog>

          <!-- 当点击表格中的数据元概念按钮时弹出该弹框,展示数据元概念信息 -->
          <el-dialog :visible.sync="dialogVisibleDataElementConcept" title="数据元概念" width="50%">
            <el-descriptions border>
              <el-descriptions-item label="数据元概念">{{
                dialogDataDataElementConcept.name
              }}</el-descriptions-item>
              <el-descriptions-item label="标识符">{{
                dialogDataDataElementConcept.identifier
              }}</el-descriptions-item>
              <el-descriptions-item label="描述">{{
                dialogDataDataElementConcept.describe
              }}</el-descriptions-item>
              <el-descriptions-item label="注册状态">{{
                dialogDataDataElementConcept.status
              }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{
                dialogDataDataElementConcept.time
              }}</el-descriptions-item>
              <el-descriptions-item label="版本">{{
                dialogDataDataElementConcept.version
              }}</el-descriptions-item>
              <el-descriptions-item label="创建人员ID">{{
                dialogDataDataElementConcept.personId
              }}</el-descriptions-item>
              <el-descriptions-item label="创建单位">{{
                dialogDataDataElementConcept.department
              }}</el-descriptions-item>
              <el-descriptions-item label="对象类">
                <span>{{ dialogDataDataElementConcept.OCLName }}</span>
                <i class="el-icon-right"></i>
                <span>{{ dialogDataDataElementConcept.OCLIdentifier }}</span>
                <span><el-link @click="
                  handleGetMDRTable(
                    dialogDataDataElementConcept.OCLIdentifier,
                    '对象类'
                  )
                  "><i class="el-icon-view el-icon--right"></i> </el-link></span>
              </el-descriptions-item>
              <el-descriptions-item label="属性">
                <span>{{ dialogDataDataElementConcept.PRPName }}</span>
                <i class="el-icon-right"></i>
                <span>{{ dialogDataDataElementConcept.PRPIdentifier }}</span>
                <span><el-link @click="
                  handleGetMDRTable(
                    dialogDataDataElementConcept.PRPIdentifier,
                    '属性'
                  )
                  "><i class="el-icon-view el-icon--right"></i> </el-link></span>
              </el-descriptions-item>
              <el-descriptions-item label="概念域">
                <span>{{ dialogDataDataElementConcept.CDMName }}</span>
                <i class="el-icon-right"></i>
                <span>{{ dialogDataDataElementConcept.CDMIdentifier }}</span>
                <span><el-link @click="
                  handleGetMDRTable(
                    dialogDataDataElementConcept.CDMIdentifier,
                    '概念域'
                  )
                  "><i class="el-icon-view el-icon--right"></i> </el-link></span>
              </el-descriptions-item>
            </el-descriptions>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisibleDataElementConcept = false">关闭</el-button>
            </span>
          </el-dialog>

          <!-- 当点击表格中的值域按钮时弹出该弹框,展示值域信息 -->
          <el-dialog :visible.sync="dialogVisibleValueDomain" title="值域" width="50%">
            <el-descriptions border>
              <el-descriptions-item label="值域">{{
                dialogDataValueDomain.name
              }}</el-descriptions-item>
              <el-descriptions-item label="标识符">{{
                dialogDataValueDomain.identifier
              }}</el-descriptions-item>
              <el-descriptions-item label="描述">{{
                dialogDataValueDomain.describe
              }}</el-descriptions-item>
              <el-descriptions-item label="注册状态">{{
                dialogDataValueDomain.status
              }}</el-descriptions-item>
              <el-descriptions-item label="创建时间">{{
                dialogDataValueDomain.time
              }}</el-descriptions-item>
              <el-descriptions-item label="版本">{{
                dialogDataValueDomain.version
              }}</el-descriptions-item>
              <el-descriptions-item label="创建人员ID">{{
                dialogDataValueDomain.personId
              }}</el-descriptions-item>
              <el-descriptions-item label="创建单位">{{
                dialogDataValueDomain.department
              }}</el-descriptions-item>
              <el-descriptions-item label="概念域">
                <span>{{ dialogDataValueDomain.CDMName }}</span>
                <i class="el-icon-right"></i>
                <span>{{ dialogDataValueDomain.CDMIdentifier }}</span>
                <span><el-link @click="
                  handleGetMDRTable(
                    dialogDataValueDomain.CDMIdentifier,
                    '概念域'
                  )
                  "><i class="el-icon-view el-icon--right"></i> </el-link></span>
              </el-descriptions-item>
            </el-descriptions>
            <el-divider content-position="center">可允许值信息</el-divider>
            <div v-if="dialogDataPermissibleValues">
              <el-descriptions v-for="(item, index) in dialogDataPermissibleValues" border style="margin-bottom: 20px"
                :column="2" :key="index">
                <el-descriptions-item label="可允许值">{{
                  item.PEVName
                }}</el-descriptions-item>
                <el-descriptions-item label="标识符">{{
                  item.PEVIdentifier
                }}</el-descriptions-item>
                <el-descriptions-item label="值含义">{{
                  item.VLMName
                }}</el-descriptions-item>
                <el-descriptions-item label="标识符">{{
                  item.VLMIdentifier
                }}</el-descriptions-item>
              </el-descriptions>
            </div>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisibleValueDomain = false">关闭</el-button>
            </span>
          </el-dialog>

          <!-- 当点击数据元表格中的标识符时弹出该弹框,展示该数据元相关的其他MDR信息图谱 -->
          <el-dialog :visible.sync="dialogVisibleGraph" title="MDR" width="60%">
            <div id="MDRGraph" style="width: 100%; height: 500px; display: flex"></div>
            <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisibleGraph = false">关闭</el-button>
            </span>
          </el-dialog>
          <!-- {% endraw %} -->
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import * as echarts from "echarts";
export default {
  data() {
    return {
      activeMenu: "",
      showTableOfObjectClass: false,
      showTableOfMDRProperty: false,
      showTableOfConceptualDomain: false,
      showTableDataElementConcept: false,
      showTableOfValueDomain: false,
      showTableOfDataElement: false,
      tableTitle: "",
      searchInput: "",
      search: "",
      tableDataOfObjectClass: [],
      tableDataOfMDRProperty: [],
      tableDataOfConceptualDomain: [],
      tableDataOfDataElementConcept: [],
      tableDataOfValueDomain: [],
      tableDataOfDataElement: [],
      dialogDataObjectClass: {},
      dialogVisibleObjectClass: false,
      dialogVisibleProperty: false,
      dialogDataProperty: {},
      dialogVisibleConceptualDomain: false,
      dialogDataConceptualDomain: {},
      dialogDataValueMenings: [],
      dialogVisibleDataElementConcept: false,
      dialogDataDataElementConcept: {},
      dialogVisibleValueDomain: false,
      dialogDataValueDomain: {},
      dialogDataPermissibleValues: [],
      selectedLabel: "",
      dialogVisibleGraph: false,
      graphData: [],
      graphLinks: [],
      categories: [
        "对象类",
        "属性",
        "概念域",
        "数据元概念",
        "值域",
        "数据元",
        "可允许值",
        "值含义",
        "值域组",
      ],
    };
  },
  mounted() {
    this.handleCommand("对象类");
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    openError() {
      this.$message.error("未查询到结果，请检查输入查询内容是否正确！");
    },
    andleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => { });
    },
    handleCommand(command) {
      var vm = this;
      this.$axios
        .get("http://127.0.0.1:5000/search/mdr/getMDRTableList", {
          params: {
            label: command,
          },
        })
        .then(function (response) {
          console.log(response)
          if (response.data.data.length == 0) {
            vm.openError();
          } else {
            vm.tableTitle = response.data.tableTitle;
            if (command === "对象类") {
              vm.showTableOfObjectClass = true;
              vm.showTableOfMDRProperty = false;
              vm.showTableOfConceptualDomain = false;
              vm.showTableDataElementConcept = false;
              vm.showTableOfValueDomain = false;
              vm.showTableOfDataElement = false;
              vm.tableDataOfObjectClass = response.data.data;
            }
            if (command == "属性") {
              vm.showTableOfMDRProperty = true;
              vm.showTableOfObjectClass = false;
              vm.showTableOfConceptualDomain = false;
              vm.showTableDataElementConcept = false;
              vm.showTableOfValueDomain = false;
              vm.showTableOfDataElement = false;
              vm.tableDataOfMDRProperty = response.data.data;
            }
            if (command == "概念域") {
              vm.showTableOfConceptualDomain = true;
              vm.showTableOfObjectClass = false;
              vm.showTableOfMDRProperty = false;
              vm.showTableDataElementConcept = false;
              vm.showTableOfValueDomain = false;
              vm.showTableOfDataElement = false;
              vm.tableDataOfConceptualDomain = response.data.data;
            }
            if (command == "数据元概念") {
              vm.showTableDataElementConcept = true;
              vm.showTableOfObjectClass = false;
              vm.showTableOfMDRProperty = false;
              vm.showTableOfConceptualDomain = false;
              vm.showTableOfValueDomain = false;
              vm.showTableOfDataElement = false;
              vm.tableDataOfDataElementConcept = response.data.data;
            }
            if (command == "值域") {
              vm.showTableOfValueDomain = true;
              vm.showTableOfMDRProperty = false;
              vm.showTableOfObjectClass = false;
              vm.showTableOfConceptualDomain = false;
              vm.showTableDataElementConcept = false;
              vm.showTableOfDataElement = false;
              vm.tableDataOfValueDomain = response.data.data;
            }
            if (command == "数据元") {
              vm.showTableOfDataElement = true;
              vm.showTableOfObjectClass = false;
              vm.showTableOfMDRProperty = false;
              vm.showTableOfConceptualDomain = false;
              vm.showTableDataElementConcept = false;
              vm.showTableOfValueDomain = false;
              vm.tableDataOfDataElement = response.data.data;
            }
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleDelete(index, row) {
      if (this.showTableOfObjectClass) {
        this.tableDataOfObjectClass.splice(index, 1); // 删除对象类的数据行
      } else if (this.showTableOfMDRProperty) {
        this.tableDataOfMDRProperty.splice(index, 1); // 删除MDR属性的数据行
      } else if (this.showTableOfConceptualDomain) {
        this.tableDataOfConceptualDomain.splice(index, 1); //删除概念域的数据行
      } else if (this.showTableDataElementConcept) {
        this.tableDataOfDataElementConcept.splice(index, 1); //删除数据元概念的数据行
      } else if (this.showTableOfValueDomain) {
        this.tableDataOfValueDomain.splice(index, 1);
      } else if (this.showTableOfDataElement) {
        this.tableDataOfDataElement.splice(index, 1);
      }
    },
    handleGetMDRTable(identifier, label) {
      var vm = this;
      // console.log(label)
      this.$axios
        .get("http://127.0.0.1:5000/search/mdr/getMDRTable", {
          params: {
            identifier: identifier,
            label: label,
          },
        })
        .then(function (response) {
          // console.log()
          if (response.data.data.length == 0) {
            vm.openError();
          } else {
            if (label == "对象类") {
              vm.dialogDataObjectClass = response.data.data[0];
              vm.dialogVisibleObjectClass = true;
            } else if (label == "属性") {
              vm.dialogDataProperty = response.data.data[0];
              vm.dialogVisibleProperty = true;
            } else if (label == "概念域") {
              vm.dialogDataConceptualDomain = response.data.data[0][0];
              vm.dialogDataValueMenings = response.data.data[1];
              // console.log(response.data.data)
              vm.dialogVisibleConceptualDomain = true;
            } else if (label == "数据元概念") {
              vm.dialogDataDataElementConcept = response.data.data[0];
              vm.dialogVisibleDataElementConcept = true;
            } else if (label == "值域") {
              vm.dialogDataValueDomain = response.data.data[0][0];
              vm.dialogDataPermissibleValues = response.data.data[1];
              vm.dialogVisibleValueDomain = true;
            }
            // vm.dialogData = response.data.data[0];
            // vm.dialogVisible = true;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getMDRGraph(identifier) {
      var vm = this;
      vm.dialogVisibleGraph = true;
      this.$axios
        .get("http://127.0.0.1:5000/search/mdr/getGraphOfMDR", {
          params: {
            identifier: identifier,
          },
        })
        .then(function (response) {
          if (response.data.data.length == 0) {
            vm.openError();
          } else {
            // console.log(response.data.data);
            vm.graphData = response.data.data.map(function (node, idx) {
              node.id = idx;
              return node;
            });
            vm.graphLinks = response.data.links;
            vm.updateChartOfMDRGraph(vm.graphData, vm.graphLinks);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    updateChartOfMDRGraph(graphData, graphLinks) {
      var myChart = echarts.init(document.getElementById("MDRGraph"));
      var vm = this;
      var option = {
        title: {
          textStyle: {
            fontWeight: "lighter",
          },
        },
        // animationDurationUpdate 设置图表更新动画的持续时间
        animationDurationUpdate: 1500,
        // animationEasingUpdate 设置图表更新动画的缓动效果
        animationEasingUpdate: "quinticInOut",
        legend: {
          x: "center",
          show: true,
          data: [
            "对象类",
            "属性",
            "概念域",
            "数据元概念",
            "值域",
            "数据元",
            "可允许值",
            "值含义",
            "值域组",
          ],
        },
        series: [
          {
            type: "graph",
            layout: "none",
            symbolSize: 60,
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [4, 4],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 12,
                },
                formatter: "{c}",
              },
            },
            force: {
              repulsion: 2500,
              edgeLength: [10, 100],
            },
            focusNodeAdjacency: true,
            draggable: true,
            roam: true,
            categories: [
              {
                name: "对象类",
              },
              {
                name: "属性",
              },
              {
                name: "概念域",
              },
              {
                name: "数据元概念",
              },
              {
                name: "值域",
              },
              {
                name: "数据元",
              },
              {
                name: "可允许值",
              },
              {
                name: "值含义",
              },
              {
                name: "值域组",
              },
            ],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 15,
                },
              },
            },
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0.01,
              },
            },
            nodes: graphData,
            links: graphLinks,
          },
        ],
      };
      myChart.setOption(option, true);
    },
  },
};
</script>

<style scoped>
.box {
  margin-left: 250px;
}

.el-menu-vertical-demo {
  height: 100vh;
}

.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}

.chat-container {
  height: 750px;
  padding: 5px;
  /* display: flex; */
  flex-direction: column;
}

.message-container {
  flex: 1;
  max-height: calc(100% - 60px);
  overflow-y: auto;
  padding-bottom: 10px;
}

.message {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  margin-bottom: 10px;
}

.message.user .message-bubble {
  margin-left: auto;
  background-color: #dcf8c6;
  color: #000;
}

.message.bot .message-bubble {
  margin-right: auto;
  background-color: #f0f0f0;
  color: #000;
}

.message-bubble {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.input-container {
  gap: 2px;
  /* margin-top: 10px; */
}

.input-container .el-input {
  flex: 2;
  width: 200px;
  border-radius: 20px;
  padding: 5px 5px;
}

.input-container button {
  flex: none;
  border-radius: 20%;
  width: 100px;
  height: 40px;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: center;
  min-height: 90vh;
}

.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}

.el-icon-arrow-down {
  font-size: 12px;
}
</style>
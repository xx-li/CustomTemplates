# -*- coding: utf-8 -*-

from common import TemplateType

# 不通过xib定义多页面视图的UI
MULTIPAGE_VIEW = """
    lazy var categoryView: DTCategoryView = DTCategoryView.init(frame: CGRect.init(x: 0, y: 0, width: 320, height: 60))
    lazy var pageView: LXMultiPageView = LXMultiPageView.init(frame: UIScreen.main.bounds)
"""

# 通过xib定义多页面视图的UI
MULTIPAGE_VIEW__XIB = """
    @IBOutlet weak var categoryView: DTCategoryView!
    @IBOutlet weak var pageView: LXMultiPageView!
"""

MULTIPAGE_VIEW_LOAD = """
        self.view.addSubview(categoryView)
        self.view.addSubview(pageView)
        categoryView.mas_makeConstraints { (make: MASConstraintMaker!) in
            make.left.right()?.offset()(0)
            if #available(iOS 11.0, *) {
                make.top.equalTo()(self.view.mas_safeAreaLayoutGuideTop)
            } else {
                make.top.offset()(64)
            }
            make.height.mas_equalTo()(60)
        }
        pageView.mas_makeConstraints { (make: MASConstraintMaker!) in
            make.left.right()?.bottom()?.offset()(0)
            make.top.equalTo()(self.categoryView.mas_bottom)
        }
"""

MULTIPAGE_VIEW_SETUP = """
        pageView.parentViewController = self
                
        self.pageView.childViewControllers = [
            UIViewController.init(),
            UIViewController.init()
        ]
        
        categoryView.titles = ["item1", "item2"]
        categoryView.sliderSize = CGSize.init(width: 12, height: 4)
        categoryView.sliderView.image = UIImage.init(named: "record_title_silder")
        categoryView.layoutType = .leftAlign
        categoryView.leftMargin = 24
        categoryView.bottomMargin = 10
        categoryView.subMargin = 28
        categoryView.selectedTitleFont = UIFont.systemFont(ofSize: 18, weight: .medium)
        categoryView.selectedTitleColor = UIColor.black.withAlphaComponent(0.85)
        categoryView.titleFont = UIFont.systemFont(ofSize: 14, weight: .regular)
        categoryView.titleColor = UIColor.black.withAlphaComponent(0.4)
        categoryView.contentScrollView = self.pageView.scrollView
        categoryView.selectedIndex = 0
"""



# 不通过xib定义tableView变量
TABLE_VIEW = """
    lazy var tableView: UITableView = {
        let tableView = UITableView.init(frame: self.view.bounds, style: .plain)
        tableView.delegate = self
        tableView.dataSource = self
        tableView.separatorStyle = .none
        return tableView
    }()
"""

# 通过xib定义tableView变量
TABLE_VIEW__XIB = "@IBOutlet weak var tableView: UITableView!"

# tableView上下拉刷新，和是否使用xib没关系
TABLE_VIEW_REFRESH = """
    let cellIdentifier = "___VARIABLE_moduleName___ListCell"

    lazy var header: MJRefreshHeader = {
        let header = DTCommon.header { [weak self] ()->(Void) in
            self?.requestList(isLoadMore: false)
        }
        tableView.mj_header = header
        return header;
    }()
    
    lazy var footer: MJRefreshFooter = {
        let footer = DTCommon.footer { [weak self] ()->(Void) in
            self?.requestList(isLoadMore: true)
        }
        tableView.mj_footer = footer
        footer.isHidden = true
        return footer
    }()
"""

# tableView 在 viewDidLoad加载（无xib）
TABLE_VIEW_LOAD = """
        view.addSubview(tableView)
        tableView.mas_makeConstraints { (make: MASConstraintMaker!) in
            make.left.right()?.bottom()?.offset()(0)
            if #available(iOS 11.0, *) {
                make.top.equalTo()(self.view.mas_safeAreaLayoutGuideTop)
            } else {
                make.top.offset()(64)
            }
        }
        tableView.register(___VARIABLE_moduleName___ListCell.self, 
                           forCellReuseIdentifier: cellIdentifier)
        // 骨架屏: https://github.com/tigerAndBull/TABAnimated
        tableView.tabAnimated = TABTableAnimated.init(cellClass: ___VARIABLE_moduleName___ListCell.self,
                                                      cellHeight: 44)
        header.beginRefreshing()
"""

# tableView 在 viewDidLoad加载（有xib）
TABLE_VIEW_LOAD__XIB = """
        tableView.register(UINib.init(nibName: cellIdentifier, bundle: nil),
                           forCellReuseIdentifier: cellIdentifier)
        // 骨架屏: https://github.com/tigerAndBull/TABAnimated
        tableView.tabAnimated = TABTableAnimated.init(cellClass: ___VARIABLE_moduleName___ListCell.self,
                                                      cellHeight: 44)
        header.beginRefreshing()
"""

# 普通页面加载数据
REQUEST_DATA = """
    // MARK: - request -

    @objc func requestData() {
        view.dt_hiddenAllEmpty()
        self.dt_request = engine.requestData() { [weak self] (isSuccess, msg) in
            guard let self = self else { return }
            if !isSuccess {
                self.view.dt_showNetworkError(
                    withTarget: self,
                    action: #selector(self.requestData)
                )
                QMUITips.show(withText: msg)
                return
            }
            
            //TODO: 更新UI
        }
    }
"""

# 列表页面加载数据
REQUEST_DATA__LIST = """
    // MARK: - request -

    @objc func requestList(isLoadMore:Bool) {
        view.dt_hiddenAllEmpty()
        self.dt_request = engine.requestList(isLoadMore: isLoadMore) { [weak self] (isSuccess, msg) in
            guard let self = self else { return }
            
            self.header.endRefreshing()
            self.footer.endRefreshing()
            self.tableView.tab_endAnimation()
            if !isSuccess {
                // 无内容时才展示网络异常页面
                if self.engine.datas.count == 0 {
                    self.view.dt_showNetworkError(
                        withTarget: self,
                        action: #selector(self.requestList(isLoadMore:))
                    )
                }
                QMUITips.show(withText: msg)
                return
            }

            self.tableView.mj_footer?.isHidden = self.engine!.dataSource.count == 0
            if self.engine.datas.count == 0 {
                self.view.dt_showNoContentView()
            } else if self.engine.isCanLoadMore() {
                self.footer.resetNoMoreData()
            } else {
                self.footer.endRefreshingWithNoMoreData()
            }
        }
    }
"""

SYNC_DATA_TO_UI = """
    func syncDataToUI(for behavior: ___VARIABLE_moduleName___Engine.ChangeBehavior) {
        //TODO: update page UI
    }
"""

SYNC_DATA_TO_UI__LIST = """
    func syncDataToUI(for behavior: ___VARIABLE_moduleName___Engine.ChangeBehavior) {
        switch behavior {
        case .add(let indexes):
            let indexPathes = indexes.map { IndexPath(row: $0, section: 0) }
            tableView.insertRows(at: indexPathes, with: .none)
        case .remove(let indexes):
            let indexPathes = indexes.map { IndexPath(row: $0, section: 0) }
            tableView.deleteRows(at: indexPathes, with: .none)
        case .reload:
            tableView.reloadData()
        case .edit(let indexes):
            let indexPathes = indexes.map { IndexPath(row: $0, section: 0) }
            tableView.reloadRows(at: indexPathes, with: .none)
        }
    }

    func updateCell(cell: ___VARIABLE_moduleName___ListCell, 
                    withModel model: ___VARIABLE_moduleName___Model) {
        //TODO: update cell UI
    }
"""

DELETE_OPERATION = """
    // MARK: - Delete Operation -

    func didClickCellDelete(at index: Int) {
        let model = engine.datas[index]
        let alertView = DTAlertView.init(title: "提示", message: "请确认是否删除此数据？")
        alertView.addAction(DTAlertAction.init(title: "取消", style: .default, handler: nil))
        alertView.addAction(DTAlertAction.init(title: "确定", style: .bold, handler: { [weak self] (DTAlertAction)->Void in
            self?.requestDelete(model: model)
        }))
        alertView.showInview(nil)
    }

    func requestDelete(model: ___VARIABLE_moduleName___Model) {
        QMUITips.showLoading(in: view)
        engine.requestOperation(behaviorType: .delete, model: model) {[weak self] (isSuccess, msg) -> (Void) in
            guard let self = self else { return }
            QMUITips.hideAllTips(in: self.view)
            QMUITips.show(withText: isSuccess ? "删除成功" : "删除失败")
        }
    }
"""

TABLE_VIEW_DELEGATE = """
// MARK: - Extensions -

// MARK: UITableViewDelegate
extension  ___VARIABLE_moduleName___ViewController: UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return engine.datas.count
    }
    
    func tableView(_ tableView: UITableView, 
                   cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let model = engine.datas[indexPath.row]
        let cell = tableView.dequeueReusableCell(
            withIdentifier: cellIdentifier, 
            for: indexPath
        ) as! ___VARIABLE_moduleName___ListCell

        updateCell(cell: cell, withModel: model)
        %TABLE_VIEW_DELEGATE_DELETE%

        return cell
    }
}


// MARK: UITableViewDelegate
extension  ___VARIABLE_moduleName___ViewController: UITableViewDelegate {
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 44
    }

    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        let model = engine.datas[indexPath.row]
        // TODO: Do something by select cell
    }
}
"""

TABLE_VIEW_DELEGATE_DELETE = """
        cell.didDeleteButtonClick = { [weak self] (cell)->(Void) in
            let indexPath = tableView.indexPath(for: cell)!
            self?.didClickCellDelete(at: indexPath.row)
        }
"""

# xib文件中的TableView
XIB_TABLEVIEW = """
            <subviews>
                <tableView clipsSubviews="YES" contentMode="scaleToFill" alwaysBounceVertical="YES" style="plain" separatorStyle="none" rowHeight="-1" estimatedRowHeight="-1" sectionHeaderHeight="28" sectionFooterHeight="28" translatesAutoresizingMaskIntoConstraints="NO" id="9ag-Xh-v5E">
                    <rect key="frame" x="0.0" y="0.0" width="414" height="808"/>
                    <color key="backgroundColor" systemColor="systemBackgroundColor"/>
                    <connections>
                        <outlet property="dataSource" destination="-1" id="xu5-h9-iZD"/>
                        <outlet property="delegate" destination="-1" id="oX8-ru-0nf"/>
                    </connections>
                </tableView>
            </subviews>
            <constraints>
                <constraint firstItem="fnl-2z-Ty3" firstAttribute="trailing" secondItem="9ag-Xh-v5E" secondAttribute="trailing" id="Od2-5j-vZQ"/>
                <constraint firstItem="9ag-Xh-v5E" firstAttribute="leading" secondItem="fnl-2z-Ty3" secondAttribute="leading" id="jxB-df-1fJ"/>
                <constraint firstItem="9ag-Xh-v5E" firstAttribute="top" secondItem="fnl-2z-Ty3" secondAttribute="top" id="mJ9-5j-9ur"/>
                <constraint firstAttribute="bottom" secondItem="9ag-Xh-v5E" secondAttribute="bottom" id="qOn-Cr-ffT"/>
            </constraints>
"""

# xib文件中TableView的outlet
XIB_TABLEVIEW_OUTLET = '<outlet property="tableView" destination="9ag-Xh-v5E" id="eQW-oy-oWB"/>'

# xib文件中的DTCategoryView 和multiPageView
XIB_MULTIPAGE_VIEW = """
            <subviews>
                <view contentMode="scaleToFill" translatesAutoresizingMaskIntoConstraints="NO" id="XFF-Fh-aKi">
                    <rect key="frame" x="0.0" y="0.0" width="414" height="61"/>
                    <viewLayoutGuide key="safeArea" id="2Bk-jP-5XI"/>
                    <color key="backgroundColor" systemColor="systemBackgroundColor"/>
                    XIB_MULTIPAGE_VIEW
                    <subviews>
                        <view contentMode="scaleToFill" translatesAutoresizingMaskIntoConstraints="NO" id="vBa-WG-U28" customClass="DTCategoryView">
                            <rect key="frame" x="0.0" y="0.0" width="414" height="56"/>
                            <color key="backgroundColor" systemColor="systemBackgroundColor"/>
                        </view>
                        <view contentMode="scaleToFill" translatesAutoresizingMaskIntoConstraints="NO" id="BNI-3Y-4Pz">
                            <rect key="frame" x="0.0" y="60" width="414" height="1"/>
                            <color key="backgroundColor" red="0.91004228590000003" green="0.92116957899999996" blue="0.94117999080000003" alpha="1" colorSpace="custom" customColorSpace="displayP3"/>
                            <constraints>
                                <constraint firstAttribute="height" constant="1" id="iTr-84-gro"/>
                            </constraints>
                        </view>
                    </subviews>
                    <constraints>
                        <constraint firstItem="vBa-WG-U28" firstAttribute="top" secondItem="XFF-Fh-aKi" secondAttribute="top" id="2v8-sK-glq"/>
                        <constraint firstItem="vBa-WG-U28" firstAttribute="leading" secondItem="XFF-Fh-aKi" secondAttribute="leading" id="4Hz-Ce-lRX"/>
                        <constraint firstAttribute="height" constant="61" id="AJa-zG-FgS"/>
                        <constraint firstAttribute="trailing" secondItem="BNI-3Y-4Pz" secondAttribute="trailing" id="Dbd-gR-IaL"/>
                        <constraint firstAttribute="trailing" secondItem="vBa-WG-U28" secondAttribute="trailing" id="ObC-WS-vnb"/>
                        <constraint firstAttribute="bottom" secondItem="BNI-3Y-4Pz" secondAttribute="bottom" id="Yib-zW-PM4"/>
                        <constraint firstItem="BNI-3Y-4Pz" firstAttribute="leading" secondItem="XFF-Fh-aKi" secondAttribute="leading" id="Zcu-eA-TmE"/>
                        <constraint firstAttribute="bottom" secondItem="vBa-WG-U28" secondAttribute="bottom" constant="5" id="uI0-j8-Crt"/>
                    </constraints>
                </view>
                <view contentMode="scaleToFill" translatesAutoresizingMaskIntoConstraints="NO" id="9R1-Iy-M4V" customClass="LXMultiPageView">
                    <rect key="frame" x="0.0" y="61" width="414" height="747"/>
                    <color key="backgroundColor" systemColor="systemBackgroundColor"/>
                </view>
            </subviews>
            <constraints>
                <constraint firstItem="XFF-Fh-aKi" firstAttribute="trailing" secondItem="fnl-2z-Ty3" secondAttribute="trailing" id="6N9-aR-Hji"/>
                <constraint firstAttribute="bottom" secondItem="9R1-Iy-M4V" secondAttribute="bottom" id="HDE-Yn-d0H"/>
                <constraint firstItem="fnl-2z-Ty3" firstAttribute="trailing" secondItem="9R1-Iy-M4V" secondAttribute="trailing" id="HmH-2Y-WyB"/>
                <constraint firstItem="XFF-Fh-aKi" firstAttribute="leading" secondItem="fnl-2z-Ty3" secondAttribute="leading" id="IrK-bh-slX"/>
                <constraint firstItem="XFF-Fh-aKi" firstAttribute="top" secondItem="fnl-2z-Ty3" secondAttribute="top" id="KBw-cz-p70"/>
                <constraint firstItem="9R1-Iy-M4V" firstAttribute="leading" secondItem="fnl-2z-Ty3" secondAttribute="leading" id="ex5-m3-jHo"/>
                <constraint firstItem="9R1-Iy-M4V" firstAttribute="top" secondItem="XFF-Fh-aKi" secondAttribute="bottom" id="gMx-rm-bsl"/>
            </constraints>
"""

# xib文件中的DTCategoryView 和multiPageView的outlet
XIB_MULTIPAGE_OUTLET = """
                <outlet property="categoryView" destination="vBa-WG-U28" id="68C-3C-Ah8"/>
                <outlet property="pageView" destination="9R1-Iy-M4V" id="u4L-xB-hRN"/>
"""


def replaceMultiPageView(vcStr, type):
    res = vcStr
    if "MultiPage" in type.value:
        res = res.replace('%MULTIPAGE_VIEW_SETUP%', MULTIPAGE_VIEW_SETUP)
        if "Xib" in type.value:
             res = res.replace('%MULTIPAGE_VIEW%', MULTIPAGE_VIEW__XIB)
             res = res.replace('%MULTIPAGE_VIEW_LOAD%', "")
        else:
            res = res.replace('%MULTIPAGE_VIEW%', MULTIPAGE_VIEW)
            res = res.replace('%MULTIPAGE_VIEW_LOAD%', MULTIPAGE_VIEW_LOAD)
    else:
        res = res.replace('%MULTIPAGE_VIEW_SETUP%', "")
        res = res.replace('%MULTIPAGE_VIEW%', "")
        res = res.replace('%MULTIPAGE_VIEW_LOAD%', "")
    return res



def replaceTableView(vcStr, type):
    res = vcStr
    if "List" in type.value:
        res = res.replace('%TABLE_VIEW_REFRESH%', TABLE_VIEW_REFRESH)
        if "Xib" in type.value:
             res = res.replace('%TABLE_VIEW%', TABLE_VIEW__XIB)
             res = res.replace('%TABLE_VIEW_LOAD%', TABLE_VIEW_LOAD__XIB)
        else:
            res = res.replace('%TABLE_VIEW%', TABLE_VIEW)
            res = res.replace('%TABLE_VIEW_LOAD%', TABLE_VIEW_LOAD)
    else:
        res = res.replace('%TABLE_VIEW%', "")
        res = res.replace('%TABLE_VIEW_REFRESH%', "")
        res = res.replace('%TABLE_VIEW_LOAD%', "requestData()")

    return res

def replaceRequestData(vcStr, type):
    res = vcStr
    if "List" in type.value:
        res = res.replace('%REQUEST_DATA%', REQUEST_DATA__LIST)
    else:
        res = res.replace('%REQUEST_DATA%', REQUEST_DATA)
        
    return res

def replaceSyncDataToUI(vcStr, type):
    res = vcStr
    if "List" in type.value:
        res = res.replace('%SYNC_DATA_TO_UI%', SYNC_DATA_TO_UI__LIST)
    else:
        res = res.replace('%SYNC_DATA_TO_UI%', SYNC_DATA_TO_UI)
        
    return res

def replaceDeleteOperation(vcStr, type):
    res = vcStr
    if "Edit" in type.value:
        res = res.replace('%DELETE_OPERATION%', DELETE_OPERATION)
    else:
        res = res.replace('%DELETE_OPERATION%', "")
    return res

def replaceTableViewDelegate(vcStr, type):
    res = vcStr
    if "List" in type.value:
        delStr = TABLE_VIEW_DELEGATE
        if "Edit" in type.value:
            delStr = delStr.replace("%TABLE_VIEW_DELEGATE_DELETE%", TABLE_VIEW_DELEGATE_DELETE)
        else:
            delStr = delStr.replace("%TABLE_VIEW_DELEGATE_DELETE%", "")
        res = res.replace('%TABLE_VIEW_DELEGATE%', delStr)
    else:
        res = res.replace('%TABLE_VIEW_DELEGATE%', "")
    return res


def replace(vcStr, type):
    res = replaceMultiPageView(vcStr, type)
    res = replaceTableView(res, type)
    res = replaceRequestData(res, type)
    res = replaceSyncDataToUI(res, type)
    res = replaceDeleteOperation(res, type)
    res = replaceTableViewDelegate(res, type)
    return res


def replaceXib(str, type):
    res = str
    if "Xib" in type.value:
        if "List" in type.value:
            res = res.replace("%XIB_TABLEVIEW%", XIB_TABLEVIEW)
            res = res.replace("%XIB_TABLEVIEW_OUTLET%", XIB_TABLEVIEW_OUTLET)
        else:
            res = res.replace("%XIB_TABLEVIEW%", "")
            res = res.replace("%XIB_TABLEVIEW_OUTLET%", "")
        
        if "MultiPage" in type.value:
            res = res.replace("%XIB_MULTIPAGE_OUTLET%", XIB_MULTIPAGE_OUTLET)
            res = res.replace("%XIB_MULTIPAGE_VIEW%", XIB_MULTIPAGE_VIEW)
        else:
            res = res.replace("%XIB_MULTIPAGE_OUTLET%", "")
            res = res.replace("%XIB_MULTIPAGE_VIEW%", "")
        
        return res
    else:
        return None

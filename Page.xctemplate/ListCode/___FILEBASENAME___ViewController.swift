//
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  Copyright (c) ___YEAR___ ___ORGANIZATIONNAME___. All rights reserved.
//
//  This file was generated by MGDT Templates
//

import UIKit

final class ___VARIABLE_moduleName___ViewController: DTBaseViewController {

    // MARK: - properties -

    

    
    lazy var tableView: UITableView = {
        let tableView = UITableView.init(frame: self.view.bounds, style: .plain)
        tableView.delegate = self
        tableView.dataSource = self
        tableView.separatorStyle = .none
        return tableView
    }()


    
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
        return footer
    }()


    let engine = ___VARIABLE_moduleName___Engine.init()

    // MARK: - Lifecycle -

    override func viewDidLoad() {
        super.viewDidLoad()

        
        

        
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


        NotificationCenter.default.addObserver(
            self,
            selector: #selector(datasDidChange),
            name: .___VARIABLE_moduleName___DidChangedNotification,
            object: nil
        )
    }

    
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
            
            if self.engine.datas.count == 0 {
                self.view.dt_showNoContentView()
            } else if self.engine.isCanLoadMore() {
                self.footer.resetNoMoreData()
            } else {
                self.footer.endRefreshingWithNoMoreData()
            }
        }
    }

    
    // MARK: - Data sync -
    
    @objc func datasDidChange(_ notification: Notification) {
        let behavior = notification.getUserInfo(
            for: .___VARIABLE_moduleName___DidChangedNotificationBehaviorKey
        )
        self.syncDataToUI(for: behavior)
    }

    // MARK: - UI -
    
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


    
}


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

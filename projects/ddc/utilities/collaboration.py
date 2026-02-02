"""
실시간 협업 시스템 - 팀 기반 분석 & 의사결정

역할:
- 실시간 협업 분석
- 공동 의사결정
- 결과 공유 & 피드백
- 팀 성과 추적
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    """사용자 역할"""
    ANALYST = "analyst"
    MANAGER = "manager"
    EXECUTIVE = "executive"
    VIEWER = "viewer"


@dataclass
class TeamMember:
    """팀 멤버"""
    id: str
    name: str
    role: UserRole
    email: str
    active: bool = True
    joined_at: datetime = field(default_factory=datetime.now)
    contributions: int = 0
    
    def has_permission(self, permission: str) -> bool:
        """권한 확인"""
        permissions = {
            UserRole.ANALYST: ['view', 'analyze', 'comment'],
            UserRole.MANAGER: ['view', 'analyze', 'comment', 'approve'],
            UserRole.EXECUTIVE: ['view', 'comment', 'decide'],
            UserRole.VIEWER: ['view']
        }
        return permission in permissions.get(self.role, [])


@dataclass
class CollaborativeAnalysis:
    """협업 분석"""
    id: str
    title: str
    creator_id: str
    status: str  # draft, in_review, approved, completed
    created_at: datetime
    updated_at: datetime
    participants: Set[str] = field(default_factory=set)
    findings: Dict[str, Any] = field(default_factory=dict)
    approvals: Dict[str, bool] = field(default_factory=dict)
    comments: List[Dict[str, Any]] = field(default_factory=list)


class CollaborationHub:
    """협업 허브"""
    
    def __init__(self):
        self.team_members: Dict[str, TeamMember] = {}
        self.active_analyses: Dict[str, CollaborativeAnalysis] = {}
        self.completed_analyses: List[CollaborativeAnalysis] = []
        self.shared_workspace = {}
        self.activity_log = []
    
    def add_team_member(self, member: TeamMember) -> Dict[str, Any]:
        """팀 멤버 추가"""
        self.team_members[member.id] = member
        
        self._log_activity('member_added', {
            'member_id': member.id,
            'name': member.name,
            'role': member.role.value
        })
        
        return {'status': 'success', 'member_id': member.id}
    
    def start_collaborative_analysis(
        self,
        title: str,
        creator_id: str,
        description: str,
        participants: List[str]
    ) -> CollaborativeAnalysis:
        """협업 분석 시작"""
        
        analysis_id = f"collab_{len(self.active_analyses)}"
        
        analysis = CollaborativeAnalysis(
            id=analysis_id,
            title=title,
            creator_id=creator_id,
            status='draft',
            created_at=datetime.now(),
            updated_at=datetime.now(),
            participants=set(participants)
        )
        
        self.active_analyses[analysis_id] = analysis
        
        self._log_activity('analysis_started', {
            'analysis_id': analysis_id,
            'title': title,
            'participants': participants
        })
        
        return analysis
    
    def add_analysis_contribution(
        self,
        analysis_id: str,
        contributor_id: str,
        contribution: Dict[str, Any]
    ) -> Dict[str, Any]:
        """분석 기여 추가"""
        
        if analysis_id not in self.active_analyses:
            return {'status': 'error', 'message': 'Analysis not found'}
        
        analysis = self.active_analyses[analysis_id]
        
        # 권한 확인
        member = self.team_members.get(contributor_id)
        if not member or not member.has_permission('analyze'):
            return {'status': 'error', 'message': 'Insufficient permissions'}
        
        # 기여 추가
        analysis.findings.update(contribution)
        analysis.participants.add(contributor_id)
        analysis.updated_at = datetime.now()
        
        # 멤버 기여도 증가
        member.contributions += 1
        
        self._log_activity('contribution_added', {
            'analysis_id': analysis_id,
            'contributor_id': contributor_id,
            'contribution_keys': list(contribution.keys())
        })
        
        return {'status': 'success', 'analysis_id': analysis_id}
    
    def submit_for_approval(
        self,
        analysis_id: str,
        submitter_id: str
    ) -> Dict[str, Any]:
        """승인 제출"""
        
        if analysis_id not in self.active_analyses:
            return {'status': 'error', 'message': 'Analysis not found'}
        
        analysis = self.active_analyses[analysis_id]
        analysis.status = 'in_review'
        
        # 승인자 목록 (매니저급)
        approvers = [
            mid for mid, m in self.team_members.items()
            if m.role in [UserRole.MANAGER, UserRole.EXECUTIVE]
        ]
        
        # 승인 초기화
        for approver in approvers:
            analysis.approvals[approver] = None  # 대기 중
        
        self._log_activity('approval_submitted', {
            'analysis_id': analysis_id,
            'submitter_id': submitter_id,
            'approvers': approvers
        })
        
        return {
            'status': 'success',
            'analysis_id': analysis_id,
            'pending_approvals': len(approvers)
        }
    
    def approve_analysis(
        self,
        analysis_id: str,
        approver_id: str,
        approved: bool,
        feedback: str = ""
    ) -> Dict[str, Any]:
        """분석 승인"""
        
        if analysis_id not in self.active_analyses:
            return {'status': 'error', 'message': 'Analysis not found'}
        
        analysis = self.active_analyses[analysis_id]
        
        # 권한 확인
        member = self.team_members.get(approver_id)
        if not member or not member.has_permission('approve'):
            return {'status': 'error', 'message': 'Insufficient permissions'}
        
        analysis.approvals[approver_id] = approved
        
        if feedback:
            analysis.comments.append({
                'user_id': approver_id,
                'timestamp': datetime.now().isoformat(),
                'text': feedback,
                'type': 'approval_feedback'
            })
        
        # 모든 승인 확인
        pending = sum(1 for v in analysis.approvals.values() if v is None)
        
        if pending == 0:
            # 모든 승인 완료
            all_approved = all(analysis.approvals.values())
            analysis.status = 'approved' if all_approved else 'rejected'
        
        self._log_activity('analysis_approved', {
            'analysis_id': analysis_id,
            'approver_id': approver_id,
            'approved': approved
        })
        
        return {
            'status': 'success',
            'analysis_id': analysis_id,
            'pending_approvals': pending
        }
    
    def add_comment(
        self,
        analysis_id: str,
        user_id: str,
        comment_text: str
    ) -> Dict[str, Any]:
        """댓글 추가"""
        
        if analysis_id not in self.active_analyses:
            return {'status': 'error', 'message': 'Analysis not found'}
        
        analysis = self.active_analyses[analysis_id]
        
        # 권한 확인
        member = self.team_members.get(user_id)
        if not member or not member.has_permission('comment'):
            return {'status': 'error', 'message': 'Insufficient permissions'}
        
        comment = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'text': comment_text,
            'type': 'comment'
        }
        
        analysis.comments.append(comment)
        
        return {'status': 'success', 'comment_id': len(analysis.comments) - 1}
    
    def get_team_dashboard(self) -> Dict[str, Any]:
        """팀 대시보드"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'team': {
                'total_members': len(self.team_members),
                'active_members': sum(1 for m in self.team_members.values() if m.active),
                'members_by_role': {
                    role.value: sum(1 for m in self.team_members.values() if m.role == role)
                    for role in UserRole
                }
            },
            'analyses': {
                'active': len(self.active_analyses),
                'completed': len(self.completed_analyses),
                'by_status': {
                    status: sum(1 for a in self.active_analyses.values() if a.status == status)
                    for status in ['draft', 'in_review', 'approved']
                }
            },
            'top_contributors': self._get_top_contributors(5),
            'recent_activity': self.activity_log[-10:]
        }
    
    def _get_top_contributors(self, limit: int = 5) -> List[Dict[str, Any]]:
        """상위 기여자"""
        sorted_members = sorted(
            self.team_members.values(),
            key=lambda m: m.contributions,
            reverse=True
        )
        
        return [
            {
                'name': m.name,
                'role': m.role.value,
                'contributions': m.contributions
            }
            for m in sorted_members[:limit]
        ]
    
    def _log_activity(self, activity_type: str, details: Dict[str, Any]):
        """활동 로그 기록"""
        self.activity_log.append({
            'timestamp': datetime.now().isoformat(),
            'type': activity_type,
            'details': details
        })
        
        # 최근 1000개만 유지
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-1000:]
    
    def export_collaboration_report(self) -> Dict[str, Any]:
        """협업 리포트 내보내기"""
        
        completed_analyses = []
        for analysis_id, analysis in self.active_analyses.items():
            if analysis.status == 'completed':
                completed_analyses.append({
                    'id': analysis.id,
                    'title': analysis.title,
                    'creator': analysis.creator_id,
                    'participants': list(analysis.participants),
                    'findings': analysis.findings,
                    'comments_count': len(analysis.comments)
                })
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_analyses': len(self.completed_analyses),
            'completed_analyses': completed_analyses,
            'team_statistics': self.get_team_dashboard()
        }


if __name__ == "__main__":
    print("👥 실시간 협업 시스템 테스트\n")
    
    hub = CollaborationHub()
    
    # 팀 구성
    members = [
        TeamMember('analyst_1', 'Alice', UserRole.ANALYST, 'alice@example.com'),
        TeamMember('manager_1', 'Bob', UserRole.MANAGER, 'bob@example.com'),
        TeamMember('exec_1', 'Charlie', UserRole.EXECUTIVE, 'charlie@example.com'),
    ]
    
    for member in members:
        hub.add_team_member(member)
    
    print("✅ 팀 구성 완료!")
    
    # 협업 분석 시작
    analysis = hub.start_collaborative_analysis(
        "Market Analysis Q1 2026",
        'analyst_1',
        "Comprehensive market analysis for Q1",
        ['analyst_1', 'manager_1', 'exec_1']
    )
    
    print(f"✅ 분석 시작: {analysis.id}")
    
    # 기여 추가
    hub.add_analysis_contribution(
        analysis.id,
        'analyst_1',
        {'market_size': '$500M', 'growth_rate': '15%'}
    )
    
    print("✅ 기여 추가 완료!")
    
    # 대시보드
    dashboard = hub.get_team_dashboard()
    print(f"\n✅ 팀 대시보드:")
    print(f"  - 활성 멤버: {dashboard['team']['active_members']}")
    print(f"  - 활성 분석: {dashboard['analyses']['active']}")
